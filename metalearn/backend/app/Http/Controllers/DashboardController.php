<?php

namespace App\Http\Controllers;

use App\Models\User;
use App\Models\UserProgress;
use App\Models\CognitiveTrace;
use App\Models\Mission;
use App\Services\AssessmentService;
use App\Services\GamificationService;
use App\Services\GeminiService;
use App\Services\MemoryService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class DashboardController extends Controller
{
    private AssessmentService $assessment;
    private GamificationService $gamification;
    private MemoryService $memory;
    private GeminiService $gemini;

    public function __construct(
        AssessmentService $assessment,
        GamificationService $gamification,
        MemoryService $memory,
        GeminiService $gemini
    ) {
        $this->assessment = $assessment;
        $this->gamification = $gamification;
        $this->memory = $memory;
        $this->gemini = $gemini;
    }

    public function studentDashboard(Request $request): JsonResponse
    {
        $user = $request->user();
        $user->load(['level.level', 'badges', 'interests', 'learningStyle']);

        $masteryProfile = $this->assessment->getMasteryProfile($user);
        $gamificationData = $this->gamification->getUserStats($user);

        $recentActivity = UserProgress::where('user_id', $user->id)
            ->with('mission')
            ->latest('completed_at')
            ->limit(5)
            ->get();

        return response()->json([
            'profile' => $user,
            'mastery' => $masteryProfile,
            'gamification' => $gamificationData,
            'recent_activity' => $recentActivity,
            'memory_context' => $this->memory->getContext($user),
        ]);
    }

    public function teacherDashboard(Request $request): JsonResponse
    {
        $students = User::where('is_active', true)
            ->whereHas('role', fn($q) => $q->where('name', 'siswa'))
            ->with(['level.level', 'progress' => fn($q) => $q->where('status', 'completed')])
            ->get()
            ->map(fn($student) => [
                'id' => $student->id,
                'name' => $student->name,
                'email' => $student->email,
                'level' => $student->level?->level?->level_number ?? 1,
                'xp' => $student->level?->current_xp ?? 0,
                'missions_completed' => $student->progress->count(),
                'last_active' => $student->progress->sortByDesc('completed_at')->first()?->completed_at,
            ]);

        $classStats = [
            'total_students' => $students->count(),
            'average_xp' => (int) $students->avg('xp'),
            'average_missions' => (int) $students->avg('missions_completed'),
            'top_student' => $students->sortByDesc('xp')->first(),
        ];

        return response()->json([
            'students' => $students,
            'class_stats' => $classStats,
        ]);
    }

    public function generateReport(Request $request): JsonResponse
    {
        $user = $request->user();
        $mastery = $this->assessment->getMasteryProfile($user);
        $memoryContent = $this->memory->getMemory($user);
        $context = $this->memory->getContext($user);

        $report = $this->gemini->generateContent(
            "Buat laporan perkembangan belajar dalam Bahasa Indonesia berdasarkan data berikut:\n\n"
            . "Data mastery: " . json_encode($mastery) . "\n"
            . "Data memori: {$memoryContent}\n"
            . "Data konteks: " . json_encode($context) . "\n\n"
            . "Format laporan:\n"
            . "1. Ringkasan progres (2-3 kalimat)\n"
            . "2. Area yang sudah dikuasai\n"
            . "3. Area yang perlu ditingkatkan\n"
            . "4. Rekomendasi belajar (3 poin)\n"
            . "5. Motivasi (1 kalimat)"
        );

        return response()->json([
            'report' => $report,
            'generated_at' => now(),
        ]);
    }
}
