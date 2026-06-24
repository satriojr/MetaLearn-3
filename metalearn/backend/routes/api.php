<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\DashboardController;
use App\Http\Controllers\GamificationController;
use App\Http\Controllers\InterestScannerController;
use App\Http\Controllers\KnowledgeMapController;
use App\Http\Controllers\LearningPathController;
use App\Http\Controllers\MemoryController;
use App\Http\Controllers\MissionController;
use App\Http\Controllers\PauseAskController;
use App\Http\Controllers\TopicController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return response()->json([
        'name' => 'MetaLearn API',
        'version' => '1.0.0',
    ]);
});

Route::post('/auth/register', [AuthController::class, 'register']);
Route::post('/auth/login', [AuthController::class, 'login']);

Route::middleware('auth:sanctum')->group(function () {
    Route::post('/auth/logout', [AuthController::class, 'logout']);
    Route::get('/auth/profile', [AuthController::class, 'profile']);

    Route::get('/topics', [TopicController::class, 'index']);
    Route::get('/topics/{topic}', [TopicController::class, 'show']);

    Route::get('/knowledge-map', [KnowledgeMapController::class, 'index']);

    Route::get('/learning-paths', [LearningPathController::class, 'index']);
    Route::get('/learning-paths/{learningPath}', [LearningPathController::class, 'show']);

    Route::get('/missions/{mission}', [MissionController::class, 'show']);
    Route::post('/missions/{mission}/start', [MissionController::class, 'start']);
    Route::post('/missions/{mission}/submit', [MissionController::class, 'submit']);

    Route::get('/scanner/questions', [InterestScannerController::class, 'getQuestions']);
    Route::post('/scanner/submit', [InterestScannerController::class, 'submit']);

    Route::post('/ai/pause-ask', [PauseAskController::class, 'ask']);

    Route::get('/gamification/stats', [GamificationController::class, 'stats']);
    Route::get('/gamification/leaderboard', [GamificationController::class, 'leaderboard']);

    Route::get('/dashboard/student', [DashboardController::class, 'studentDashboard']);
    Route::get('/dashboard/teacher', [DashboardController::class, 'teacherDashboard']);
    Route::get('/dashboard/report', [DashboardController::class, 'generateReport']);

    Route::get('/memory', [MemoryController::class, 'show']);
    Route::delete('/memory', [MemoryController::class, 'destroy']);
});
