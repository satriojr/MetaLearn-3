<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('missions', function (Blueprint $table) {
            $table->id();
            $table->foreignId('learning_path_id')->constrained()->cascadeOnDelete();
            $table->string('title', 200);
            $table->enum('type', ['quiz', 'reading', 'interactive', 'project'])->default('quiz');
            $table->unsignedTinyInteger('difficulty')->default(1);
            $table->integer('xp_reward')->default(0);
            $table->unsignedSmallInteger('estimated_minutes')->default(10);
            $table->unsignedSmallInteger('sequence_order')->default(0);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('missions');
    }
};
