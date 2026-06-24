<?php

namespace App\Http\Controllers;

use App\Models\Interest;
use App\Models\LearningStyle;
use App\Services\MemoryService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class InterestScannerController extends Controller
{
    private MemoryService $memory;

    public function __construct(MemoryService $memory)
    {
        $this->memory = $memory;
    }

    public function getQuestions(): JsonResponse
    {
        $interests = Interest::all();
        $learningStyles = LearningStyle::all();

        return response()->json([
            'questions' => [
                [
                    'id' => 'interests',
                    'type' => 'multiple_select',
                    'question' => 'Mata pelajaran apa yang paling kamu sukai? (Pilih minimal 2)',
                    'options' => $interests->map(fn($i) => [
                        'id' => $i->id,
                        'label' => $i->name,
                        'icon' => $i->icon,
                        'color' => $i->color,
                    ]),
                ],
                [
                    'id' => 'learning_style',
                    'type' => 'single_select',
                    'question' => 'Bagaimana cara kamu paling mudah belajar?',
                    'options' => $learningStyles->map(fn($ls) => [
                        'id' => $ls->id,
                        'label' => $ls->name,
                        'description' => $ls->description,
                    ]),
                ],
                [
                    'id' => 'goals',
                    'type' => 'single_select',
                    'question' => 'Apa tujuan utama kamu belajar?',
                    'options' => [
                        ['id' => 'nilai', 'label' => 'Mendapatkan nilai bagus'],
                        ['id' => 'paham', 'label' => 'Memahami konsep secara mendalam'],
                        ['id' => 'lomba', 'label' => 'Persiapan lomba/olimpiade'],
                        ['id' => 'eksplor', 'label' => 'Eksplorasi minat baru'],
                    ],
                ],
                [
                    'id'          => 'session_duration',
                    'type'        => 'duration',
                    'question'    => 'Berapa menit waktu idealmu untuk satu sesi belajar?',
                    'description' => 'Geser slider untuk memilih durasi. AI akan mengatur jadwal belajarmu sesuai pilihanmu.',
                    'options'     => [],
                ],
            ],
        ]);
    }

    public function submit(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'interest_ids'     => 'required|array|min:2',
            'interest_ids.*'   => 'exists:interests,id',
            'learning_style_id'=> 'required|exists:learning_styles,id',
            'goals'            => 'sometimes|string|nullable',
            'session_duration' => 'required|integer|min:5|max:120',
        ]);

        $user = $request->user();

        $user->interests()->sync($validated['interest_ids']);
        $user->learning_style_id = $validated['learning_style_id'];
        $user->save();

        $learningStyle = LearningStyle::find($validated['learning_style_id']);
        $interests = Interest::whereIn('id', $validated['interest_ids'])->get();

        $this->memory->initialize($user, [
            'learning_style_code' => $learningStyle?->code ?? 'visual',
            'learning_style_name' => $learningStyle?->name ?? 'Visual',
            'interest_names' => $interests->pluck('name')->toArray(),
        ]);

        $this->memory->updateContext($user, [
            'ai_flags' => [
                'learning_style_id' => $learningStyle?->code ?? 'visual',
                'preferred_session_duration_min' => (int) $validated['session_duration'],
            ],
        ]);

        return response()->json([
            'message' => 'Profil berhasil disimpan',
            'user' => $user->load(['interests', 'learningStyle']),
        ]);
    }
}
