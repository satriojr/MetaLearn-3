<?php

namespace App\Http\Controllers;

use App\Models\Mission;
use App\Services\GeminiService;
use App\Services\MemoryService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class PauseAskController extends Controller
{
    private GeminiService $gemini;
    private MemoryService $memory;

    public function __construct(GeminiService $gemini, MemoryService $memory)
    {
        $this->gemini = $gemini;
        $this->memory = $memory;
    }

    public function ask(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'question' => 'required|string|max:1000',
            'mission_id' => 'nullable|exists:missions,id',
            'context' => 'nullable|string|max:500',
        ]);

        $user = $request->user();

        $ragChunks = $this->memory->getRagChunks($user, $validated['question']);

        $contextData = [
            'memory' => $this->memory->getMemory($user),
            'rag_chunks' => $ragChunks,
        ];

        $missionContext = '';
        if (!empty($validated['mission_id'])) {
            $mission = Mission::with('questions')->find($validated['mission_id']);
            if ($mission) {
                $missionContext = "Konteks materi: {$mission->title}\n"
                    . "Topik terkait: " . ($mission->learningPath?->name ?? '') . "\n";
            }
        }

        $prompt = "Seorang siswa sedang belajar dan mengajukan pertanyaan berikut:\n\n"
            . "Pertanyaan: {$validated['question']}\n\n"
            . "{$missionContext}"
            . "Konteks tambahan: {$validated['context']}\n\n"
            . "Berikan jawaban yang jelas, ramah, dan mendidik dalam Bahasa Indonesia. "
            . "Sertakan contoh sederhana jika relevan. Jika pertanyaan di luar materi, arahkan kembali ke topik belajar.";

        $answer = $this->gemini->generateContent($prompt, $contextData);

        return response()->json([
            'question' => $validated['question'],
            'answer' => $answer,
        ]);
    }
}
