<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $this->call([
            RoleSeeder::class,
            LearningStyleSeeder::class,
            InterestSeeder::class,
            LevelSeeder::class,
            BadgeSeeder::class,
            TopicSeeder::class,
            QuestionBankSeeder::class,
            UserSeeder::class,
        ]);
    }
}
