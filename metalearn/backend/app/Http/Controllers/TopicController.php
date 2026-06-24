<?php

namespace App\Http\Controllers;

use App\Models\Topic;
use Illuminate\Http\JsonResponse;

class TopicController extends Controller
{
    public function index(): JsonResponse
    {
        $topics = Topic::with(['learningPaths' => function ($q) {
            $q->where('is_active', true)->orderBy('sequence_order');
        }])->get();

        return response()->json($topics);
    }

    public function show(Topic $topic): JsonResponse
    {
        $topic->load(['learningPaths.missions' => function ($q) {
            $q->orderBy('sequence_order');
        }]);

        return response()->json($topic);
    }
}
