<?php

namespace App\Services;

use App\Models\Badge;
use App\Models\Level;
use App\Models\User;
use App\Models\UserLevel;
use App\Models\UserProgress;
use Illuminate\Support\Facades\DB;

class GamificationService
{
    public function awardXp(User $user, int $xp): array
    {
        $userLevel = UserLevel::firstOrCreate(
            ['user_id' => $user->id],
            ['current_xp' => 0, 'level_id' => 1]
        );

        $userLevel->increment('current_xp', $xp);

        $currentLevel = Level::find($userLevel->level_id);
        $nextLevel = Level::where('level_number', '>', $currentLevel->level_number)
            ->orderBy('level_number')
            ->first();

        $leveledUp = false;
        while ($nextLevel && $userLevel->current_xp >= $nextLevel->min_xp) {
            $userLevel->level_id = $nextLevel->id;
            $userLevel->save();
            $leveledUp = true;

            $currentLevel = $nextLevel;
            $nextLevel = Level::where('level_number', '>', $currentLevel->level_number)
                ->orderBy('level_number')
                ->first();
        }

        $newBadges = $this->checkBadges($user, $userLevel);

        return [
            'xp_earned' => $xp,
            'total_xp' => $userLevel->current_xp,
            'level' => $currentLevel ? [
                'number' => $currentLevel->level_number,
                'title' => $currentLevel->title,
            ] : null,
            'leveled_up' => $leveledUp,
            'new_badges' => $newBadges,
        ];
    }

    public function getUserStats(User $user): array
    {
        $userLevel = $user->level;
        $level = $userLevel?->level;

        $completedMissions = UserProgress::where('user_id', $user->id)
            ->where('status', 'completed')
            ->count();

        $totalMissions = UserProgress::where('user_id', $user->id)->count();

        return [
            'xp' => $userLevel?->current_xp ?? 0,
            'level' => $level ? [
                'number' => $level->level_number,
                'title' => $level->title,
                'min_xp' => $level->min_xp,
                'max_xp' => $level->max_xp,
            ] : null,
            'next_level_xp' => $this->getNextLevelXp($userLevel?->current_xp ?? 0),
            'badges' => $user->badges()->get()->toArray(),
            'completed_missions' => $completedMissions,
            'total_missions' => $totalMissions,
        ];
    }

    public function getLeaderboard(?int $topicId = null): array
    {
        $query = UserLevel::with(['user', 'level'])
            ->whereHas('user', fn($q) => $q->where('is_active', true))
            ->orderByDesc('current_xp')
            ->limit(50);

        if ($topicId) {
            $query->whereHas('user.progress', fn($q) => $q->whereHas('mission.learningPath', fn($qq) => $qq->where('topic_id', $topicId)));
        }

        return $query->get()->map(fn($ul, $idx) => [
            'rank' => $idx + 1,
            'user' => [
                'id' => $ul->user->id,
                'name' => $ul->user->name,
            ],
            'xp' => $ul->current_xp,
            'level' => $ul->level?->level_number ?? 1,
        ])->toArray();
    }

    private function checkBadges(User $user, UserLevel $userLevel): array
    {
        $earned = [];

        $badges = Badge::whereDoesntHave('users', fn($q) => $q->where('user_id', $user->id))->get();

        $completedMissions = UserProgress::where('user_id', $user->id)
            ->where('status', 'completed')->count();

        foreach ($badges as $badge) {
            $earnedIt = match ($badge->criteria_type) {
                'xp_threshold' => $userLevel->current_xp >= (int) $badge->criteria_value,
                'level_reach' => ($userLevel->level?->level_number ?? 1) >= (int) $badge->criteria_value,
                'missions_completed', 'mission_complete' => $completedMissions >= (int) $badge->criteria_value,
                'streak' => false,
                default => false,
            };

            if ($earnedIt) {
                DB::table('user_badges')->insert([
                    'user_id' => $user->id,
                    'badge_id' => $badge->id,
                    'earned_at' => now(),
                ]);
                $earned[] = $badge->toArray();
            }
        }

        return $earned;
    }

    private function getNextLevelXp(int $currentXp): ?int
    {
        $next = Level::where('min_xp', '>', $currentXp)
            ->orderBy('min_xp')
            ->first();
        return $next?->min_xp;
    }
}
