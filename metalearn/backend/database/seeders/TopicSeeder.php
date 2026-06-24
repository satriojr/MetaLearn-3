<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class TopicSeeder extends Seeder
{
    public function run(): void
    {
        if (DB::table('topics')->exists()) { return; }
        // ============== MATEMATIKA ==============
        $mathId = DB::table('topics')->insertGetId([
            'name'        => 'Matematika',
            'description' => 'Ilmu tentang bilangan, struktur, ruang, dan perubahan',
            'icon'        => 'calculator',
            'color_hex'   => '#6366f1',
            'category'    => 'saintek',
        ]);

        $aljabarId = DB::table('learning_paths')->insertGetId([
            'topic_id'        => $mathId,
            'name'            => 'Aljabar Linear',
            'difficulty_level'=> 'beginner',
            'description'     => 'Memahami variabel, persamaan, dan operasi aljabar dasar',
            'sequence_order'  => 1,
            'is_active'       => true,
        ]);
        $geometriId = DB::table('learning_paths')->insertGetId([
            'topic_id'        => $mathId,
            'name'            => 'Geometri Bidang',
            'difficulty_level'=> 'beginner',
            'description'     => 'Mempelajari bangun datar, luas, dan keliling',
            'sequence_order'  => 2,
            'is_active'       => true,
        ]);
        $trigId = DB::table('learning_paths')->insertGetId([
            'topic_id'        => $mathId,
            'name'            => 'Trigonometri Dasar',
            'difficulty_level'=> 'intermediate',
            'description'     => 'Memahami sinus, cosinus, tangen, dan aplikasinya',
            'sequence_order'  => 3,
            'is_active'       => true,
        ]);

        DB::table('missions')->insert([
            ['learning_path_id' => $aljabarId, 'title' => 'Pengenalan Variabel',     'type' => 'quiz',        'difficulty' => 1, 'xp_reward' => 50,  'estimated_minutes' => 10, 'sequence_order' => 1],
            ['learning_path_id' => $aljabarId, 'title' => 'Operasi Aljabar Dasar',   'type' => 'quiz',        'difficulty' => 1, 'xp_reward' => 60,  'estimated_minutes' => 15, 'sequence_order' => 2],
            ['learning_path_id' => $geometriId,'title' => 'Bangun Dasar',             'type' => 'interactive', 'difficulty' => 1, 'xp_reward' => 50,  'estimated_minutes' => 10, 'sequence_order' => 1],
            ['learning_path_id' => $trigId,    'title' => 'Sinus, Cosinus, Tangen',  'type' => 'quiz',        'difficulty' => 2, 'xp_reward' => 80,  'estimated_minutes' => 20, 'sequence_order' => 1],
        ]);

        // ============== FISIKA ==============
        $fisikaId = DB::table('topics')->insertGetId([
            'name'        => 'Fisika',
            'description' => 'Ilmu alam yang mempelajari materi, gerak, energi, dan gaya',
            'icon'        => 'atom',
            'color_hex'   => '#06b6d4',
            'category'    => 'saintek',
        ]);

        $mekanikId = DB::table('learning_paths')->insertGetId([
            'topic_id'        => $fisikaId,
            'name'            => 'Mekanika Dasar',
            'difficulty_level'=> 'beginner',
            'description'     => 'Hukum Newton, gerak, dan gaya',
            'sequence_order'  => 1,
            'is_active'       => true,
        ]);
        $energiId = DB::table('learning_paths')->insertGetId([
            'topic_id'        => $fisikaId,
            'name'            => 'Energi & Usaha',
            'difficulty_level'=> 'intermediate',
            'description'     => 'Konsep energi kinetik, potensial, dan usaha',
            'sequence_order'  => 2,
            'is_active'       => true,
        ]);

        DB::table('missions')->insert([
            ['learning_path_id' => $mekanikId, 'title' => 'Hukum Newton I & II',   'type' => 'quiz', 'difficulty' => 1, 'xp_reward' => 55,  'estimated_minutes' => 12, 'sequence_order' => 1],
            ['learning_path_id' => $mekanikId, 'title' => 'Gerak Lurus Beraturan',  'type' => 'quiz', 'difficulty' => 1, 'xp_reward' => 60,  'estimated_minutes' => 15, 'sequence_order' => 2],
            ['learning_path_id' => $energiId,  'title' => 'Energi Kinetik & Potensial', 'type' => 'quiz', 'difficulty' => 2, 'xp_reward' => 70, 'estimated_minutes' => 20, 'sequence_order' => 1],
        ]);

        // ============== KIMIA ==============
        $kimiaId = DB::table('topics')->insertGetId([
            'name'        => 'Kimia',
            'description' => 'Ilmu yang mempelajari komposisi, struktur, dan sifat materi',
            'icon'        => 'flask',
            'color_hex'   => '#10b981',
            'category'    => 'saintek',
        ]);

        $atomId = DB::table('learning_paths')->insertGetId([
            'topic_id'        => $kimiaId,
            'name'            => 'Struktur Atom',
            'difficulty_level'=> 'beginner',
            'description'     => 'Mengenal proton, neutron, elektron, dan konfigurasi elektron',
            'sequence_order'  => 1,
            'is_active'       => true,
        ]);

        DB::table('missions')->insert([
            ['learning_path_id' => $atomId, 'title' => 'Mengenal Atom & Unsur',  'type' => 'quiz', 'difficulty' => 1, 'xp_reward' => 50, 'estimated_minutes' => 10, 'sequence_order' => 1],
            ['learning_path_id' => $atomId, 'title' => 'Tabel Periodik Dasar',   'type' => 'quiz', 'difficulty' => 1, 'xp_reward' => 55, 'estimated_minutes' => 12, 'sequence_order' => 2],
        ]);

        // ============== BIOLOGI ==============
        $bioId = DB::table('topics')->insertGetId([
            'name'        => 'Biologi',
            'description' => 'Ilmu yang mempelajari makhluk hidup dan proses kehidupan',
            'icon'        => 'leaf',
            'color_hex'   => '#84cc16',
            'category'    => 'saintek',
        ]);

        $selId = DB::table('learning_paths')->insertGetId([
            'topic_id'        => $bioId,
            'name'            => 'Sel & Jaringan',
            'difficulty_level'=> 'beginner',
            'description'     => 'Memahami sel sebagai unit terkecil kehidupan',
            'sequence_order'  => 1,
            'is_active'       => true,
        ]);

        DB::table('missions')->insert([
            ['learning_path_id' => $selId, 'title' => 'Sel Prokariot & Eukariot', 'type' => 'quiz', 'difficulty' => 1, 'xp_reward' => 50, 'estimated_minutes' => 10, 'sequence_order' => 1],
        ]);

        // ============== BAHASA INDONESIA ==============
        $bahasaId = DB::table('topics')->insertGetId([
            'name'        => 'Bahasa Indonesia',
            'description' => 'Pengembangan kemampuan berbahasa Indonesia dengan baik dan benar',
            'icon'        => 'book',
            'color_hex'   => '#f59e0b',
            'category'    => 'humaniora',
        ]);

        $kalimatId = DB::table('learning_paths')->insertGetId([
            'topic_id'        => $bahasaId,
            'name'            => 'Kalimat Efektif',
            'difficulty_level'=> 'beginner',
            'description'     => 'Menyusun kalimat yang efektif dan komunikatif',
            'sequence_order'  => 1,
            'is_active'       => true,
        ]);

        DB::table('missions')->insert([
            ['learning_path_id' => $kalimatId, 'title' => 'Struktur Kalimat Dasar', 'type' => 'quiz', 'difficulty' => 1, 'xp_reward' => 45, 'estimated_minutes' => 10, 'sequence_order' => 1],
        ]);

        // ============== SEJARAH ==============
        $sejarahId = DB::table('topics')->insertGetId([
            'name'        => 'Sejarah',
            'description' => 'Mempelajari peristiwa masa lalu untuk memahami masa kini',
            'icon'        => 'landmark',
            'color_hex'   => '#ec4899',
            'category'    => 'humaniora',
        ]);

        $proklamasiId = DB::table('learning_paths')->insertGetId([
            'topic_id'        => $sejarahId,
            'name'            => 'Proklamasi & Kemerdekaan RI',
            'difficulty_level'=> 'beginner',
            'description'     => 'Peristiwa-peristiwa penting menjelang dan sesudah proklamasi 1945',
            'sequence_order'  => 1,
            'is_active'       => true,
        ]);

        DB::table('missions')->insert([
            ['learning_path_id' => $proklamasiId, 'title' => 'Peristiwa Rengasdengklok', 'type' => 'quiz', 'difficulty' => 1, 'xp_reward' => 45, 'estimated_minutes' => 10, 'sequence_order' => 1],
        ]);
    }
}
