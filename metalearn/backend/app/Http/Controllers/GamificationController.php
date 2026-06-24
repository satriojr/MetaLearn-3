<?php

namespace App\Http\Controllers;

use App\Services\GamificationService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class GamificationController extends Controller
{
    private GamificationService $gamification;

    public function __construct(GamificationService $gamification)
    {
        $this->gamification = $gamification;
    }

    public function stats(Request $request): JsonResponse
    {
        return response()->json(
            $this->gamification->getUserStats($request->user())
        );
    }

    public function leaderboard(Request $request): JsonResponse
    {
        $topicId = $request->query('topic_id');

        return response()->json(
            $this->gamification->getLeaderboard($topicId ? (int) $topicId : null)
        );
    }
}
