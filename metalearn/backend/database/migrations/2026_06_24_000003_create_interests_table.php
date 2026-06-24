<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('interests', function (Blueprint $table) {
            $table->id();
            $table->string('name', 100);
            $table->string('icon', 50)->nullable();
            $table->string('color', 20)->nullable();
            $table->timestamps();
        });

        Schema::create('user_interests', function (Blueprint $table) {
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->foreignId('interest_id')->constrained()->cascadeOnDelete();
            $table->primary(['user_id', 'interest_id']);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('user_interests');
        Schema::dropIfExists('interests');
    }
};
