<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class LevelSeeder extends Seeder
{
    public function run(): void
    {
        $levels = [
            ['level_number' => 1, 'title' => 'Pelajar Pemula', 'min_xp' => 0, 'max_xp' => 99],
            ['level_number' => 2, 'title' => 'Pelajar Aktif', 'min_xp' => 100, 'max_xp' => 299],
            ['level_number' => 3, 'title' => 'Pelajar Tekun', 'min_xp' => 300, 'max_xp' => 599],
            ['level_number' => 4, 'title' => 'Pelajar Rajin', 'min_xp' => 600, 'max_xp' => 999],
            ['level_number' => 5, 'title' => 'Pelajar Teladan', 'min_xp' => 1000, 'max_xp' => 1499],
            ['level_number' => 6, 'title' => 'Sarjana Muda', 'min_xp' => 1500, 'max_xp' => 2199],
            ['level_number' => 7, 'title' => 'Sarjana', 'min_xp' => 2200, 'max_xp' => 2999],
            ['level_number' => 8, 'title' => 'Master', 'min_xp' => 3000, 'max_xp' => 3999],
            ['level_number' => 9, 'title' => 'Doktor', 'min_xp' => 4000, 'max_xp' => 5499],
            ['level_number' => 10, 'title' => 'Profesor', 'min_xp' => 5500, 'max_xp' => 999999],
        ];

        DB::table('levels')->insert($levels);
    }
}
