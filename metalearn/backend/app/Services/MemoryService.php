<?php

namespace App\Services;

use App\Models\User;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Storage;

class MemoryService
{
    private string $disk;
    private GeminiService $gemini;

    public function __construct(GeminiService $gemini)
    {
        $this->gemini = $gemini;
        $this->disk = config('filesystems.default');
    }

    public function initialize(User $user, array $profileData): void
    {
        $path = "users/{$user->id}/.ai";

        $context = [
            'user_id' => "usr_{$user->id}",
            'session_count' => 0,
            'last_session' => now()->toIso8601String(),
            'active_learning_path' => null,
            'mastery_scores' => new \stdClass(),
            'gamification' => [
                'total_xp' => 0,
                'level' => 1,
                'active_badges' => [],
                'streak_days' => 0,
            ],
            'ai_flags' => [
                'confusion_zones' => [],
                'learning_style_id' => $profileData['learning_style_code'] ?? 'visual',
                'preferred_session_duration_min' => 30,
                'pause_ask_frequency' => 'low',
            ],
        ];

        $memoryMd = "# Memori Belajar: {$user->name}\n"
            . "**Terakhir diperbarui:** " . now()->format('Y-m-d H:i') . " WIB\n\n"
            . "## Profil Singkat\n"
            . "- Gaya belajar dominan: " . ($profileData['learning_style_name'] ?? 'Visual') . "\n"
            . "- Minat: " . implode(', ', $profileData['interest_names'] ?? []) . "\n\n"
            . "## Progres Terkini\n"
            . "- Misi selesai: 0\n"
            . "- XP total: 0\n"
            . "- Level: 1\n\n"
            . "## Catatan Awal\n"
            . "- Pengguna baru bergabung pada " . now()->format('Y-m-d') . "\n";

        Storage::disk($this->disk)->put("{$path}/context.json", json_encode($context, JSON_PRETTY_PRINT));
        Storage::disk($this->disk)->put("{$path}/memory.md", $memoryMd);
    }

    public function getContext(User $user): array
    {
        $path = "users/{$user->id}/.ai/context.json";
        if (!Storage::disk($this->disk)->exists($path)) {
            return [];
        }
        return json_decode(Storage::disk($this->disk)->get($path), true) ?? [];
    }

    public function getMemory(User $user): string
    {
        $path = "users/{$user->id}/.ai/memory.md";
        if (!Storage::disk($this->disk)->exists($path)) {
            return '';
        }
        return Storage::disk($this->disk)->get($path);
    }

    public function updateContext(User $user, array $data): void
    {
        $path = "users/{$user->id}/.ai/context.json";
        $context = $this->getContext($user);
        $context = array_replace_recursive($context, $data);
        $context['last_session'] = now()->toIso8601String();
        Storage::disk($this->disk)->put($path, json_encode($context, JSON_PRETTY_PRINT));
    }

    public function appendMemory(User $user, string $newContent): void
    {
        $path = "users/{$user->id}/.ai/memory.md";
        $existing = $this->getMemory($user);
        $updated = $existing . "\n\n" . $newContent;
        Storage::disk($this->disk)->put($path, $updated);
    }

    public function writePostSessionSummary(User $user, array $sessionData): void
    {
        $summary = $this->gemini->generateContent(
            "Buat ringkasan sesi belajar dalam bahasa Indonesia dalam format Markdown dengan bagian:\n"
            . "- **Aktivitas**: apa yang dipelajari\n"
            . "- **Pencapaian**: skor, XP didapat\n"
            . "- **Kesulitan**: topik yang masih membingungkan\n"
            . "- **Saran**: rekomendasi untuk sesi berikutnya\n\n"
            . "Data sesi: " . json_encode($sessionData),
            ['memory' => $this->getMemory($user)]
        );

        $entry = "## Ringkasan Sesi " . now()->format('Y-m-d H:i') . "\n{$summary}";
        $this->appendMemory($user, $entry);

        $this->updateContext($user, [
            'session_count' => ($this->getContext($user)['session_count'] ?? 0) + 1,
        ]);
    }

    public function getRagChunks(User $user, string $query, int $limit = 5): array
    {
        return [];
    }

    public function deleteMemory(User $user): void
    {
        $path = "users/{$user->id}/.ai";
        Storage::disk($this->disk)->deleteDirectory($path);
    }
}
