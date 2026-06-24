<?php

namespace App\Services;

use App\Models\CognitiveTrace;
use App\Models\Question;
use App\Models\User;
use App\Models\UserProgress;
use Illuminate\Support\Facades\DB;

class AssessmentService
{
    private GeminiService $gemini;
    private GamificationService $gamification;
    private MemoryService $memory;

    public function __construct(
        GeminiService $gemini,
        GamificationService $gamification,
        MemoryService $memory
    ) {
        $this->gemini = $gemini;
        $this->gamification = $gamification;
        $this->memory = $memory;
    }

    public function evaluateAnswer(User $user, Question $question, mixed $userAnswer, array $traceData = []): array
    {
        $this->recordTrace($user, $question, 'submit', $traceData);

        $isCorrect = false;
        $score = 0;
        $feedback = '';

        if ($question->type === 'multiple_choice') {
            $isCorrect = (string) $userAnswer === (string) $question->correct_answer;
            $score = $isCorrect ? $question->xp_value : 0;
            $feedback = $isCorrect
                ? ($question->explanation ?? 'Jawaban benar!')
                : ($question->explanation ?? 'Jawaban kurang tepat. Coba pelajari lagi materinya.');
        } elseif ($question->type === 'short_answer') {
            $result = $this->evaluateWithAi($user, $question, $userAnswer);
            $isCorrect = $result['is_correct'];
            $score = $result['score'];
            $feedback = $result['feedback'];
        } else {
            $result = $this->evaluateWithAi($user, $question, $userAnswer);
            $isCorrect = $result['is_correct'];
            $score = $result['score'];
            $feedback = $result['feedback'];
        }

        return [
            'is_correct' => $isCorrect,
            'score' => $score,
            'feedback' => $feedback,
            'xp_earned' => $score,
        ];
    }

    public function submitMission(User $user, int $missionId, array $answers): array
    {
        $totalScore = 0;
        $maxScore = 0;
        $results = [];

        DB::beginTransaction();
        try {
            $mission = \App\Models\Mission::with('questions')->findOrFail($missionId);

            foreach ($mission->questions as $question) {
                $userAnswer = $answers[$question->id] ?? null;
                $maxScore += $question->xp_value;

                if ($userAnswer === null) {
                    $results[$question->id] = [
                        'is_correct' => false,
                        'score' => 0,
                        'feedback' => 'Tidak dijawab',
                        'xp_earned' => 0,
                    ];
                    continue;
                }

                $result = $this->evaluateAnswer($user, $question, $userAnswer);
                $totalScore += $result['score'];
                $results[$question->id] = $result;
            }

            $xpEarned = (int) round(($totalScore / max($maxScore, 1)) * ($mission->xp_reward ?? 50));

            $progress = UserProgress::updateOrCreate(
                ['user_id' => $user->id, 'mission_id' => $missionId],
                [
                    'status' => 'completed',
                    'score' => $maxScore > 0 ? round(($totalScore / $maxScore) * 100) : 0,
                    'xp_earned' => $xpEarned,
                    'attempts' => DB::raw('COALESCE(attempts, 0) + 1'),
                    'completed_at' => now(),
                ]
            );

            $gamificationResult = $this->gamification->awardXp($user, $xpEarned);

            $this->memory->updateContext($user, [
                'gamification' => [
                    'total_xp' => ($user->level?->current_xp ?? 0) + $xpEarned,
                    'level' => $gamificationResult['level']['number'] ?? 1,
                ],
            ]);

            DB::commit();

            return [
                'mission_id' => $missionId,
                'score_pct' => $progress->score,
                'xp_earned' => $xpEarned,
                'results' => $results,
                'gamification' => $gamificationResult,
            ];
        } catch (\Exception $e) {
            DB::rollBack();
            throw $e;
        }
    }

    public function getMasteryProfile(User $user): array
    {
        $progress = UserProgress::where('user_id', $user->id)
            ->with('mission.learningPath.topic')
            ->where('status', 'completed')
            ->get();

        $masteryByTopic = [];
        foreach ($progress as $p) {
            $topicName = $p->mission->learningPath->topic->name ?? 'Unknown';
            if (!isset($masteryByTopic[$topicName])) {
                $masteryByTopic[$topicName] = ['total' => 0, 'earned' => 0];
            }
            $masteryByTopic[$topicName]['total']++;
            $masteryByTopic[$topicName]['earned'] += $p->score;
        }

        $scores = [];
        foreach ($masteryByTopic as $topic => $data) {
            $scores[$topic] = $data['total'] > 0 ? round($data['earned'] / $data['total']) : 0;
        }

        $traceCount = CognitiveTrace::where('user_id', $user->id)->count();
        $confusionZones = CognitiveTrace::where('user_id', $user->id)
            ->where('action_type', 'pause')
            ->with('question.mission.learningPath')
            ->get()
            ->groupBy(fn($t) => $t->question?->mission?->learningPath?->name ?? 'unknown')
            ->map(fn($group) => $group->count())
            ->sortDesc()
            ->take(3)
            ->keys()
            ->toArray();

        return [
            'mastery_scores' => $scores,
            'total_traces' => $traceCount,
            'confusion_zones' => $confusionZones,
            'total_missions_completed' => $progress->count(),
        ];
    }

    private function evaluateWithAi(User $user, Question $question, mixed $userAnswer): array
    {
        $context = [
            'memory' => $this->memory->getMemory($user),
        ];

        $prompt = "Evaluasi jawaban siswa berikut untuk soal:\n\n"
            . "Soal: {$question->question_text}\n"
            . "Jawaban benar: {$question->correct_answer}\n"
            . "Jawaban siswa: " . (is_string($userAnswer) ? $userAnswer : json_encode($userAnswer)) . "\n\n"
            . "Penjelasan soal: {$question->explanation}\n\n"
            . "Tentukan apakah jawaban siswa benar secara konseptual (tidak harus persis sama teksnya).\n"
            . "Respond in JSON format:\n"
            . '{"is_correct": true/false, "score": 0-100, "feedback": "penjelasan dalam Bahasa Indonesia"}';

        return $this->gemini->generateJson($prompt, $context);
    }

    private function recordTrace(User $user, Question $question, string $actionType, array $data): void
    {
        CognitiveTrace::create([
            'user_id' => $user->id,
            'question_id' => $question->id,
            'action_type' => $actionType,
            'duration_ms' => $data['duration_ms'] ?? null,
            'payload' => $data,
            'recorded_at' => now(),
        ]);
    }
}
