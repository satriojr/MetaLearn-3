<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class GeminiService
{
    private string $apiKey;
    private string $apiUrl;
    private string $model;

    public function __construct()
    {
        $this->apiKey = config('services.gemini.api_key');
        $this->model = config('services.gemini.model', 'gemini-1.5-flash');
        $this->apiUrl = "https://generativelanguage.googleapis.com/v1beta/models/{$this->model}:generateContent";
    }

    public function generateContent(string $prompt, array $context = []): string
    {
        $systemInstruction = $this->buildSystemInstruction($context);

        $payload = [
            'system_instruction' => [
                'parts' => [['text' => $systemInstruction]],
            ],
            'contents' => [
                [
                    'role' => 'user',
                    'parts' => [['text' => $prompt]],
                ],
            ],
            'generationConfig' => [
                'temperature' => 0.7,
                'maxOutputTokens' => 2048,
            ],
        ];

        $response = Http::timeout(30)
            ->withHeaders(['Content-Type' => 'application/json', 'X-Goog-Api-Key' => $this->apiKey])
            ->post($this->apiUrl, $payload);

        if ($response->failed()) {
            Log::error('Gemini API error', [
                'status' => $response->status(),
                'body' => $response->body(),
            ]);
            throw new \RuntimeException('Gagal menghubungi AI: ' . $response->body());
        }

        $data = $response->json();
        return $data['candidates'][0]['content']['parts'][0]['text'] ?? '';
    }

    public function generateJson(string $prompt, array $context = []): array
    {
        $jsonPrompt = $prompt . "\n\nRespond only with valid JSON, no markdown formatting.";

        $systemInstruction = $this->buildSystemInstruction($context);

        $payload = [
            'system_instruction' => [
                'parts' => [['text' => $systemInstruction]],
            ],
            'contents' => [
                [
                    'role' => 'user',
                    'parts' => [['text' => $jsonPrompt]],
                ],
            ],
            'generationConfig' => [
                'temperature' => 0.3,
                'maxOutputTokens' => 4096,
            ],
        ];

        $response = Http::timeout(30)
            ->withHeaders(['Content-Type' => 'application/json', 'X-Goog-Api-Key' => $this->apiKey])
            ->post($this->apiUrl, $payload);

        if ($response->failed()) {
            Log::error('Gemini API error (JSON)', [
                'status' => $response->status(),
                'body' => $response->body(),
            ]);
            throw new \RuntimeException('Gagal menghubungi AI: ' . $response->body());
        }

        $data = $response->json();
        $text = $data['candidates'][0]['content']['parts'][0]['text'] ?? '';

        $text = preg_replace('/```(?:json)?\s*/', '', $text);
        $text = trim($text);

        $decoded = json_decode($text, true);
        if (json_last_error() !== JSON_ERROR_NONE) {
            Log::warning('Gemini returned invalid JSON', ['text' => $text]);
            return [];
        }

        return $decoded;
    }

    private function buildSystemInstruction(array $context): string
    {
        $instruction = "Kamu adalah MetaLearn AI — asisten pembelajaran adaptif untuk siswa sekolah menengah Indonesia. "
            . "Gunakan bahasa Indonesia yang ramah dan mudah dipahami. "
            . "Kamu membantu siswa belajar dengan memberikan penjelasan, soal, dan umpan balik yang personal.";

        if (!empty($context['memory'])) {
            $instruction .= "\n\n## KONTEKS SISWA\n" . $context['memory'];
        }

        if (!empty($context['rag_chunks'])) {
            $instruction .= "\n\n## RIWAYAT BELAJAR TERKAIT\n" . implode("\n---\n", $context['rag_chunks']);
        }

        return $instruction;
    }
}
