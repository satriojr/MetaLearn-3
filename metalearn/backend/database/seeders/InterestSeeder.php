<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class InterestSeeder extends Seeder
{
    public function run(): void
    {
        if (DB::table('interests')->exists()) { return; }
        DB::table('interests')->insert([
            ['name' => 'Matematika', 'icon' => 'calculator', 'color' => '#6366f1'],
            ['name' => 'Fisika', 'icon' => 'atom', 'color' => '#ef4444'],
            ['name' => 'Kimia', 'icon' => 'flask', 'color' => '#8b5cf6'],
            ['name' => 'Biologi', 'icon' => 'dna', 'color' => '#22c55e'],
            ['name' => 'Bahasa Indonesia', 'icon' => 'book', 'color' => '#f59e0b'],
            ['name' => 'Bahasa Inggris', 'icon' => 'globe', 'color' => '#3b82f6'],
            ['name' => 'Sejarah', 'icon' => 'landmark', 'color' => '#ec4899'],
            ['name' => 'Geografi', 'icon' => 'map', 'color' => '#14b8a6'],
            ['name' => 'Informatika', 'icon' => 'monitor', 'color' => '#06b6d4'],
            ['name' => 'Seni Budaya', 'icon' => 'palette', 'color' => '#f97316'],
        ]);
    }
}
