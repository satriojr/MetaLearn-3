<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('question_bank', function (Blueprint $table) {
            $table->id();
            $table->foreignId('mission_id')->constrained()->cascadeOnDelete();
            $table->enum('type', ['multiple_choice', 'short_answer', 'drag_drop'])->default('multiple_choice');
            $table->text('question_text');
            $table->text('correct_answer')->nullable();
            $table->text('explanation')->nullable();
            $table->string('structure_answer', 50)->nullable();
            $table->integer('xp_value')->default(10);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('question_bank');
    }
};
