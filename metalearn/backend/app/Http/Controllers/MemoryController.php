<?php

namespace App\Http\Controllers;

use App\Services\MemoryService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class MemoryController extends Controller
{
    private MemoryService $memory;

    public function __construct(MemoryService $memory)
    {
        $this->memory = $memory;
    }

    public function show(Request $request): JsonResponse
    {
        $user = $request->user();

        return response()->json([
            'memory' => $this->memory->getMemory($user),
            'context' => $this->memory->getContext($user),
        ]);
    }

    public function destroy(Request $request): JsonResponse
    {
        $this->memory->deleteMemory($request->user());

        return response()->json(['message' => 'Memori berhasil dihapus.']);
    }
}
