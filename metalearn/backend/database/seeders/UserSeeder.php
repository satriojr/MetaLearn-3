<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class UserSeeder extends Seeder
{
    public function run(): void
    {
        if (User::where('email', 'teacher@metalearn.dev')->exists()) { return; }
        User::create([
            'name' => 'Teacher MetaLearn',
            'email' => 'teacher@metalearn.dev',
            'password' => Hash::make('password123'),
            'role_id' => 2,
            'learning_style_id' => 1,
            'is_active' => true,
        ]);

        User::create([
            'name' => 'Admin MetaLearn',
            'email' => 'admin@metalearn.dev',
            'password' => Hash::make('password123'),
            'role_id' => 3,
            'learning_style_id' => 1,
            'is_active' => true,
        ]);

        User::create([
            'name' => 'Budi Santoso',
            'email' => 'budi@example.com',
            'password' => Hash::make('password123'),
            'role_id' => 1,
            'learning_style_id' => 1,
            'is_active' => true,
        ]);

        User::create([
            'name' => 'Siti Rahmawati',
            'email' => 'siti@example.com',
            'password' => Hash::make('password123'),
            'role_id' => 1,
            'learning_style_id' => 2,
            'is_active' => true,
        ]);

        User::create([
            'name' => 'Ahmad Fauzi',
            'email' => 'ahmad@example.com',
            'password' => Hash::make('password123'),
            'role_id' => 1,
            'learning_style_id' => 3,
            'is_active' => true,
        ]);

        User::create([
            'name' => 'Dewi Lestari',
            'email' => 'dewi@example.com',
            'password' => Hash::make('password123'),
            'role_id' => 1,
            'learning_style_id' => 4,
            'is_active' => true,
        ]);

        User::create([
            'name' => 'Rudi Hartono',
            'email' => 'rudi@example.com',
            'password' => Hash::make('password123'),
            'role_id' => 1,
            'learning_style_id' => 5,
            'is_active' => false,
        ]);
    }
}
