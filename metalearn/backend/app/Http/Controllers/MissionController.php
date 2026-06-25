<?php

namespace App\Http\Controllers;

use App\Models\Mission;
use App\Models\UserProgress;
use App\Services\AssessmentService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class MissionController extends Controller
{
    private AssessmentService $assessment;

    public function __construct(AssessmentService $assessment)
    {
        $this->assessment = $assessment;
    }

    public function show(Mission $mission): JsonResponse
    {
        $mission->load(['learningPath.topic', 'questions.options']);

        if (auth()->user()?->isSiswa()) {
            $progress = UserProgress::where('user_id', auth()->id())
                ->where('mission_id', $mission->id)
                ->first();

            return response()->json([
                'mission' => $mission,
                'progress' => $progress,
            ]);
        }

        return response()->json(['mission' => $mission]);
    }

    public function start(Request $request, Mission $mission): JsonResponse
    {
        $user = $request->user();

        UserProgress::firstOrCreate(
            ['user_id' => $user->id, 'mission_id' => $mission->id],
            ['status' => 'in_progress']
        );

        $mission->load(['questions.options']);

        return response()->json([
            'message' => 'Misi dimulai',
            'mission' => $mission,
        ]);
    }

    public function submit(Request $request, Mission $mission): JsonResponse
    {
        $validated = $request->validate([
            'answers'        => 'required|array',
            'answers.*'      => 'required',
            'traces'         => 'sometimes|array',
            'traces.*.question_id' => 'sometimes|integer',
            'traces.*.action_type' => 'sometimes|string',
            'traces.*.duration_ms' => 'sometimes|integer',
            'traces.*.payload'     => 'sometimes|array',
        ]);

        $user = $request->user();

        $result = $this->assessment->submitMission(
            $user,
            $mission->id,
            $validated['answers'],
            $validated['traces'] ?? []
        );

        return response()->json($result);
    }
}
