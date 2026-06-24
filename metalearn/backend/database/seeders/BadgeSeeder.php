<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class BadgeSeeder extends Seeder
{
    public function run(): void
    {
        if (DB::table('badges')->exists()) { return; }
        DB::table('badges')->insert([
            ['name' => 'Perintis', 'description' => 'Menyelesaikan misi pertama', 'icon' => 'rocket', 'criteria_type' => 'mission_complete', 'criteria_value' => '1'],
            ['name' => 'Ninja Fokus', 'description' => 'Sesi belajar tanpa interupsi ≥ 30 menit', 'icon' => 'focus', 'criteria_type' => 'ai_dynamic', 'criteria_value' => 'focus_30min'],
            ['name' => 'Penjelajah Konsep', 'description' => 'Menjelajahi ≥ 5 topik berbeda dalam seminggu', 'icon' => 'compass', 'criteria_type' => 'ai_dynamic', 'criteria_value' => 'explore_5topics'],
            ['name' => 'Pantang Menyerah', 'description' => 'Melakukan revisi ≥ 3 kali sebelum benar', 'icon' => 'shield', 'criteria_type' => 'ai_dynamic', 'criteria_value' => 'retry_3times'],
            ['name' => 'Guru Kecil', 'description' => 'Skor sempurna pada topik tertentu 3x berturut-turut', 'icon' => 'graduation', 'criteria_type' => 'ai_dynamic', 'criteria_value' => 'perfect_3streak'],
            ['name' => 'Kolektor XP', 'description' => 'Mengumpulkan 1.000 XP total', 'icon' => 'star', 'criteria_type' => 'xp_threshold', 'criteria_value' => '1000'],
            ['name' => 'Rajin Belajar', 'description' => 'Aktif belajar 7 hari berturut-turut', 'icon' => 'fire', 'criteria_type' => 'streak', 'criteria_value' => '7'],
        ]);
    }
}
