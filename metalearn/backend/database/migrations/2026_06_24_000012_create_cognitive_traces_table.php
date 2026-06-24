<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('cognitive_traces', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('question_id')->constrained('question_bank')->cascadeOnDelete();
            $table->enum('action_type', ['click', 'pause', 'revise', 'submit'])->default('click');
            $table->integer('duration_ms')->default(0);
            $table->json('payload')->nullable();
            $table->timestamp('recorded_at')->useCurrent();

            $table->index(['user_id', 'recorded_at']);
            $table->index(['user_id', 'action_type']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('cognitive_traces');
    }
};
