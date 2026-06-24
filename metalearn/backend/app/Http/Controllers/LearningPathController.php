<?php

namespace App\Http\Controllers;

use App\Models\LearningPath;
use Illuminate\Http\JsonResponse;

class LearningPathController extends Controller
{
    public function index(): JsonResponse
    {
        $paths = LearningPath::with('topic')
            ->where('is_active', true)
            ->orderBy('sequence_order')
            ->get();

        return response()->json($paths);
    }

    public function show(LearningPath $learningPath): JsonResponse
    {
        $learningPath->load(['topic', 'missions' => function ($q) {
            $q->orderBy('sequence_order');
        }]);

        return response()->json($learningPath);
    }
}
