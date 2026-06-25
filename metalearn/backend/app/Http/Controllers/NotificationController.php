<?php

namespace App\Http\Controllers;

use App\Events\NotificationCreated;
use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Notifications\DatabaseNotification;

class NotificationController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $notifications = $request->user()
            ->notifications()
            ->orderBy('created_at', 'desc')
            ->take(50)
            ->get()
            ->map(fn (DatabaseNotification $n) => [
                'id' => $n->id,
                'type' => $n->type,
                'data' => $n->data,
                'read_at' => $n->read_at,
                'created_at' => $n->created_at,
            ]);

        return response()->json($notifications);
    }

    public function unreadCount(Request $request): JsonResponse
    {
        $count = $request->user()->unreadNotifications()->count();

        return response()->json(['count' => $count]);
    }

    public function markAsRead(Request $request, string $id): JsonResponse
    {
        $notification = $request->user()
            ->notifications()
            ->where('id', $id)
            ->firstOrFail();

        $notification->markAsRead();

        return response()->json(['message' => 'Notification marked as read.']);
    }

    public function markAllAsRead(Request $request): JsonResponse
    {
        $request->user()->unreadNotifications()->update(['read_at' => now()]);

        return response()->json(['message' => 'All notifications marked as read.']);
    }

    public function sendTest(Request $request): JsonResponse
    {
        $request->validate([
            'user_id' => 'required|integer|exists:users,id',
            'title' => 'required|string|max:255',
            'body' => 'required|string',
            'type' => 'required|string|in:badge_earned,mission_completed,level_up,system',
        ]);

        $currentUser = $request->user();
        if (!$currentUser->isGuru() && !$currentUser->isAdmin()) {
            return response()->json(['message' => 'Forbidden.'], 403);
        }

        $user = User::findOrFail($request->user_id);

        $notificationData = [
            'title' => $request->title,
            'body' => $request->body,
            'type' => $request->type,
            'time' => now()->toISOString(),
        ];

        $notification = $user->notifications()->create([
            'id' => (string) \Illuminate\Support\Str::uuid(),
            'type' => $request->type,
            'data' => $notificationData,
        ]);

        NotificationCreated::dispatch(
            $user->id,
            [
                'id' => $notification->id,
                'type' => $request->type,
                'data' => $notificationData,
                'read_at' => null,
                'created_at' => $notification->created_at,
            ]
        );

        return response()->json(['message' => 'Test notification sent.']);
    }
}
