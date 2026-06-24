<?php

namespace App\Http\Controllers;

use App\Models\Topic;
use App\Models\UserProgress;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class KnowledgeMapController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $user = $request->user();

        $topics = Topic::with(['learningPaths.missions' => function ($q) {
            $q->orderBy('sequence_order');
        }])->get();

        $completedMissions = UserProgress::where('user_id', $user->id)
            ->where('status', 'completed')
            ->with('mission.learningPath')
            ->get();

        $masteryByTopic = [];
        foreach ($completedMissions as $progress) {
            $topicName = $progress->mission?->learningPath?->topic?->name;
            if (!$topicName) continue;

            if (!isset($masteryByTopic[$topicName])) {
                $masteryByTopic[$topicName] = ['total' => 0, 'earned' => 0];
            }
            $masteryByTopic[$topicName]['total']++;
            $masteryByTopic[$topicName]['earned'] += $progress->score;
        }

        $enriched = $topics->map(function ($topic) use ($masteryByTopic) {
            $data = $masteryByTopic[$topic->name] ?? null;
            $mastery = $data ? round($data['earned'] / $data['total']) : 0;

            $pathCount = $topic->learningPaths->count();
            $missionsCompleted = 0;
            $totalMissions = 0;

            foreach ($topic->learningPaths as $path) {
                $totalMissions += $path->missions->count();
            }

            return [
                'id' => $topic->id,
                'name' => $topic->name,
                'description' => $topic->description,
                'icon' => $topic->icon,
                'color_hex' => $topic->color_hex,
                'category' => $topic->category,
                'mastery' => $mastery,
                'path_count' => $pathCount,
                'total_missions' => $totalMissions,
                'learning_paths' => $topic->learningPaths->map(fn($path) => [
                    'id' => $path->id,
                    'name' => $path->name,
                    'difficulty_level' => $path->difficulty_level,
                    'description' => $path->description,
                    'mission_count' => $path->missions->count(),
                    'missions' => $path->missions->map(fn($m) => [
                        'id' => $m->id,
                        'title' => $m->title,
                        'type' => $m->type,
                        'difficulty' => $m->difficulty,
                        'xp_reward' => $m->xp_reward,
                        'estimated_minutes' => $m->estimated_minutes,
                    ]),
                ]),
            ];
        });

        return response()->json([
            'topics' => $enriched,
        ]);
    }
}
