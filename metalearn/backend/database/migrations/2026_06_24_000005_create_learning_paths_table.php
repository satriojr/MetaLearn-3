<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('learning_paths', function (Blueprint $table) {
            $table->id();
            $table->foreignId('topic_id')->constrained()->cascadeOnDelete();
            $table->string('name', 150);
            $table->enum('difficulty_level', ['beginner', 'intermediate', 'advanced'])->default('beginner');
            $table->text('description')->nullable();
            $table->unsignedSmallInteger('sequence_order')->default(0);
            $table->boolean('is_active')->default(true);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('learning_paths');
    }
};
