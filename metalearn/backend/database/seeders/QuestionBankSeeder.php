<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class QuestionBankSeeder extends Seeder
{
    public function run(): void
    {
        // Get missions
        $missions = DB::table('missions')->get()->keyBy('title');

        // ===== Pengenalan Variabel =====
        $m1 = $missions->get('Pengenalan Variabel');
        if ($m1) {
            $q1 = DB::table('question_bank')->insertGetId([
                'mission_id'     => $m1->id,
                'type'           => 'multiple_choice',
                'question_text'  => 'Dalam persamaan 3x + 5 = 20, nilai x yang memenuhi persamaan adalah...',
                'correct_answer' => '5',
                'explanation'    => 'Dari 3x + 5 = 20, maka 3x = 15, sehingga x = 5.',
                'xp_value'       => 10,
            ]);
            DB::table('answer_options')->insert([
                ['question_id' => $q1, 'option_text' => '3', 'is_correct' => false],
                ['question_id' => $q1, 'option_text' => '5', 'is_correct' => true],
                ['question_id' => $q1, 'option_text' => '7', 'is_correct' => false],
                ['question_id' => $q1, 'option_text' => '15', 'is_correct' => false],
            ]);

            $q2 = DB::table('question_bank')->insertGetId([
                'mission_id'     => $m1->id,
                'type'           => 'multiple_choice',
                'question_text'  => 'Manakah yang merupakan contoh variabel dalam matematika?',
                'correct_answer' => 'x',
                'explanation'    => 'Variabel adalah simbol (biasanya huruf) yang mewakili nilai yang belum diketahui. Contoh: x, y, n.',
                'xp_value'       => 10,
            ]);
            DB::table('answer_options')->insert([
                ['question_id' => $q2, 'option_text' => '7', 'is_correct' => false],
                ['question_id' => $q2, 'option_text' => 'x', 'is_correct' => true],
                ['question_id' => $q2, 'option_text' => '3.14', 'is_correct' => false],
                ['question_id' => $q2, 'option_text' => '100', 'is_correct' => false],
            ]);

            $q3 = DB::table('question_bank')->insertGetId([
                'mission_id'     => $m1->id,
                'type'           => 'multiple_choice',
                'question_text'  => 'Jika a = 4 dan b = 3, maka nilai 2a + 3b adalah...',
                'correct_answer' => '17',
                'explanation'    => '2(4) + 3(3) = 8 + 9 = 17.',
                'xp_value'       => 10,
            ]);
            DB::table('answer_options')->insert([
                ['question_id' => $q3, 'option_text' => '14', 'is_correct' => false],
                ['question_id' => $q3, 'option_text' => '17', 'is_correct' => true],
                ['question_id' => $q3, 'option_text' => '20', 'is_correct' => false],
                ['question_id' => $q3, 'option_text' => '21', 'is_correct' => false],
            ]);

            $q4 = DB::table('question_bank')->insertGetId([
                'mission_id'     => $m1->id,
                'type'           => 'short_answer',
                'question_text'  => 'Jelaskan apa yang dimaksud dengan variabel dalam matematika dan berikan satu contoh penggunaannya dalam kehidupan sehari-hari!',
                'correct_answer' => 'Variabel adalah simbol yang mewakili nilai tidak diketahui, contoh: jarak = kecepatan × waktu (d = v × t)',
                'explanation'    => 'Variabel memungkinkan kita membuat formula umum yang berlaku untuk berbagai situasi berbeda.',
                'xp_value'       => 20,
            ]);
        }

        // ===== Operasi Aljabar Dasar =====
        $m2 = $missions->get('Operasi Aljabar Dasar');
        if ($m2) {
            $q5 = DB::table('question_bank')->insertGetId([
                'mission_id'     => $m2->id,
                'type'           => 'multiple_choice',
                'question_text'  => 'Sederhanakan: 3x + 2y + 5x - y',
                'correct_answer' => '8x + y',
                'explanation'    => 'Kumpulkan suku sejenis: (3x + 5x) + (2y - y) = 8x + y.',
                'xp_value'       => 15,
            ]);
            DB::table('answer_options')->insert([
                ['question_id' => $q5, 'option_text' => '8x + y', 'is_correct' => true],
                ['question_id' => $q5, 'option_text' => '8x + 3y', 'is_correct' => false],
                ['question_id' => $q5, 'option_text' => '8xy', 'is_correct' => false],
                ['question_id' => $q5, 'option_text' => '6x + y', 'is_correct' => false],
            ]);

            $q6 = DB::table('question_bank')->insertGetId([
                'mission_id'     => $m2->id,
                'type'           => 'multiple_choice',
                'question_text'  => 'Hasil dari (x + 3)(x + 2) adalah...',
                'correct_answer' => 'x² + 5x + 6',
                'explanation'    => 'Menggunakan FOIL: x·x + x·2 + 3·x + 3·2 = x² + 2x + 3x + 6 = x² + 5x + 6.',
                'xp_value'       => 15,
            ]);
            DB::table('answer_options')->insert([
                ['question_id' => $q6, 'option_text' => 'x² + 5x + 6', 'is_correct' => true],
                ['question_id' => $q6, 'option_text' => 'x² + 6x + 6', 'is_correct' => false],
                ['question_id' => $q6, 'option_text' => 'x² + 5x + 5', 'is_correct' => false],
                ['question_id' => $q6, 'option_text' => 'x² + 3x + 2', 'is_correct' => false],
            ]);

            $q7 = DB::table('question_bank')->insertGetId([
                'mission_id'     => $m2->id,
                'type'           => 'multiple_choice',
                'question_text'  => 'Nilai dari 2(3x - 4) ketika x = 3 adalah...',
                'correct_answer' => '10',
                'explanation'    => '2(3(3) - 4) = 2(9 - 4) = 2(5) = 10.',
                'xp_value'       => 15,
            ]);
            DB::table('answer_options')->insert([
                ['question_id' => $q7, 'option_text' => '8', 'is_correct' => false],
                ['question_id' => $q7, 'option_text' => '10', 'is_correct' => true],
                ['question_id' => $q7, 'option_text' => '14', 'is_correct' => false],
                ['question_id' => $q7, 'option_text' => '18', 'is_correct' => false],
            ]);
        }

        // ===== Bangun Dasar (Geometri) =====
        $m3 = $missions->get('Bangun Dasar');
        if ($m3) {
            $q8 = DB::table('question_bank')->insertGetId([
                'mission_id'     => $m3->id,
                'type'           => 'multiple_choice',
                'question_text'  => 'Luas persegi dengan sisi 7 cm adalah...',
                'correct_answer' => '49 cm²',
                'explanation'    => 'Luas persegi = sisi × sisi = 7 × 7 = 49 cm².',
                'xp_value'       => 10,
            ]);
            DB::table('answer_options')->insert([
                ['question_id' => $q8, 'option_text' => '28 cm²', 'is_correct' => false],
                ['question_id' => $q8, 'option_text' => '49 cm²', 'is_correct' => true],
                ['question_id' => $q8, 'option_text' => '14 cm²', 'is_correct' => false],
                ['question_id' => $q8, 'option_text' => '56 cm²', 'is_correct' => false],
            ]);

            $q9 = DB::table('question_bank')->insertGetId([
                'mission_id'     => $m3->id,
                'type'           => 'multiple_choice',
                'question_text'  => 'Keliling lingkaran dengan diameter 14 cm adalah... (π ≈ 22/7)',
                'correct_answer' => '44 cm',
                'explanation'    => 'Keliling = π × diameter = (22/7) × 14 = 44 cm.',
                'xp_value'       => 15,
            ]);
            DB::table('answer_options')->insert([
                ['question_id' => $q9, 'option_text' => '44 cm', 'is_correct' => true],
                ['question_id' => $q9, 'option_text' => '154 cm', 'is_correct' => false],
                ['question_id' => $q9, 'option_text' => '28 cm', 'is_correct' => false],
                ['question_id' => $q9, 'option_text' => '88 cm', 'is_correct' => false],
            ]);

            $q10 = DB::table('question_bank')->insertGetId([
                'mission_id'     => $m3->id,
                'type'           => 'multiple_choice',
                'question_text'  => 'Sebuah segitiga memiliki alas 10 cm dan tinggi 8 cm. Luasnya adalah...',
                'correct_answer' => '40 cm²',
                'explanation'    => 'Luas segitiga = ½ × alas × tinggi = ½ × 10 × 8 = 40 cm².',
                'xp_value'       => 15,
            ]);
            DB::table('answer_options')->insert([
                ['question_id' => $q10, 'option_text' => '80 cm²', 'is_correct' => false],
                ['question_id' => $q10, 'option_text' => '40 cm²', 'is_correct' => true],
                ['question_id' => $q10, 'option_text' => '18 cm²', 'is_correct' => false],
                ['question_id' => $q10, 'option_text' => '20 cm²', 'is_correct' => false],
            ]);
        }

        // ===== Sinus, Cosinus, Tangen =====
        $m4 = $missions->get('Sinus, Cosinus, Tangen');
        if ($m4) {
            $q11 = DB::table('question_bank')->insertGetId([
                'mission_id'     => $m4->id,
                'type'           => 'multiple_choice',
                'question_text'  => 'Nilai sin 30° adalah...',
                'correct_answer' => '1/2',
                'explanation'    => 'sin 30° = 1/2 adalah nilai trigonometri dasar yang perlu dihafalkan.',
                'xp_value'       => 20,
            ]);
            DB::table('answer_options')->insert([
                ['question_id' => $q11, 'option_text' => '√3/2', 'is_correct' => false],
                ['question_id' => $q11, 'option_text' => '1/2', 'is_correct' => true],
                ['question_id' => $q11, 'option_text' => '√2/2', 'is_correct' => false],
                ['question_id' => $q11, 'option_text' => '1', 'is_correct' => false],
            ]);

            $q12 = DB::table('question_bank')->insertGetId([
                'mission_id'     => $m4->id,
                'type'           => 'multiple_choice',
                'question_text'  => 'Nilai cos 60° adalah...',
                'correct_answer' => '1/2',
                'explanation'    => 'cos 60° = 1/2. Perhatikan: cos 60° = sin 30°.',
                'xp_value'       => 20,
            ]);
            DB::table('answer_options')->insert([
                ['question_id' => $q12, 'option_text' => '0', 'is_correct' => false],
                ['question_id' => $q12, 'option_text' => '√3/2', 'is_correct' => false],
                ['question_id' => $q12, 'option_text' => '1/2', 'is_correct' => true],
                ['question_id' => $q12, 'option_text' => '1', 'is_correct' => false],
            ]);

            $q13 = DB::table('question_bank')->insertGetId([
                'mission_id'     => $m4->id,
                'type'           => 'multiple_choice',
                'question_text'  => 'Dalam segitiga siku-siku, tan θ didefinisikan sebagai...',
                'correct_answer' => 'sisi depan / sisi samping',
                'explanation'    => 'tan θ = sisi depan / sisi samping (opposite / adjacent). Ingat: SOH-CAH-TOA.',
                'xp_value'       => 20,
            ]);
            DB::table('answer_options')->insert([
                ['question_id' => $q13, 'option_text' => 'sisi depan / hipotenusa', 'is_correct' => false],
                ['question_id' => $q13, 'option_text' => 'sisi samping / hipotenusa', 'is_correct' => false],
                ['question_id' => $q13, 'option_text' => 'sisi depan / sisi samping', 'is_correct' => true],
                ['question_id' => $q13, 'option_text' => 'hipotenusa / sisi depan', 'is_correct' => false],
            ]);

            $q14 = DB::table('question_bank')->insertGetId([
                'mission_id'     => $m4->id,
                'type'           => 'short_answer',
                'question_text'  => 'Sebuah tangga bersandar ke tembok dengan sudut 60° ke tanah. Jika panjang tangga 8 meter, berapa tinggi tembok yang dicapai tangga? (gunakan sin 60° = √3/2 ≈ 0.866)',
                'correct_answer' => '4√3 meter atau sekitar 6.93 meter',
                'explanation'    => 'Tinggi = panjang tangga × sin 60° = 8 × (√3/2) = 4√3 ≈ 6.93 meter.',
                'xp_value'       => 30,
            ]);
        }
    }
}
