<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class RoleSeeder extends Seeder
{
    public function run(): void
    {
        DB::table('roles')->insert([
            ['name' => 'siswa', 'description' => 'Siswa - pengguna utama platform'],
            ['name' => 'guru', 'description' => 'Guru / tenaga pendidik'],
            ['name' => 'admin', 'description' => 'Administrator platform'],
        ]);
    }
}
