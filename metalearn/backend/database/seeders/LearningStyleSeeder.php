<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class LearningStyleSeeder extends Seeder
{
    public function run(): void
    {
        if (DB::table('learning_styles')->exists()) { return; }
        DB::table('learning_styles')->insert([
            ['code' => 'visual', 'name' => 'Visual', 'description' => 'Belajar optimal melalui gambar, diagram, dan video'],
            ['code' => 'auditory', 'name' => 'Auditori', 'description' => 'Belajar optimal melalui pendengaran dan diskusi'],
            ['code' => 'kinesthetic', 'name' => 'Kinestetik', 'description' => 'Belajar optimal melalui praktik dan gerakan'],
            ['code' => 'reading_writing', 'name' => 'Membaca-Menulis', 'description' => 'Belajar optimal melalui teks dan catatan'],
            ['code' => 'visual_kinesthetic', 'name' => 'Visual-Kinestetik', 'description' => 'Kombinasi visual dan praktik langsung'],
        ]);
    }
}
