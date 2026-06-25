<?php

namespace App\Http\Controllers;

use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class ChatController extends Controller
{
    private string $aiServiceUrl;

    public function __construct()
    {
        $this->aiServiceUrl = rtrim(env('AI_SERVICE_URL', 'http://ai-service:8001'), '/');
    }

    public function send(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'message' => 'required|string|max:2000',
            'session_id' => 'nullable|string|max:100',
        ]);

        $response = Http::timeout(30)->post("{$this->aiServiceUrl}/chat/send", [
            'message' => $validated['message'],
            'session_id' => $validated['session_id'] ?? null,
        ]);

        if ($response->failed()) {
            return response()->json([
                'reply' => 'Maaf, layanan AI sedang sibuk. Silakan coba lagi.',
            ], 502);
        }

        return response()->json($response->json());
    }

    public function reset(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'session_id' => 'required|string|max:100',
        ]);

        $response = Http::timeout(10)->post("{$this->aiServiceUrl}/chat/reset", [
            'session_id' => $validated['session_id'],
        ]);

        if ($response->failed()) {
            return response()->json(['message' => 'Gagal mereset percakapan.'], 500);
        }

        return response()->json($response->json());
    }
}
