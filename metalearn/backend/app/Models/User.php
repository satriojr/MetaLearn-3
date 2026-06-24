<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, Notifiable;

    protected $fillable = [
        'name', 'email', 'password', 'role_id', 'learning_style_id', 'is_active',
    ];

    protected $hidden = [
        'password', 'remember_token',
    ];

    public function role()
    {
        return $this->belongsTo(Role::class);
    }

    public function learningStyle()
    {
        return $this->belongsTo(LearningStyle::class);
    }

    public function interests()
    {
        return $this->belongsToMany(Interest::class, 'user_interests');
    }

    public function progress()
    {
        return $this->hasMany(UserProgress::class);
    }

    public function cognitiveTraces()
    {
        return $this->hasMany(CognitiveTrace::class);
    }

    public function badges()
    {
        return $this->belongsToMany(Badge::class, 'user_badges')->withPivot('earned_at');
    }

    public function level()
    {
        return $this->hasOne(UserLevel::class);
    }

    public function isSiswa(): bool
    {
        return $this->role?->name === 'siswa';
    }

    public function isGuru(): bool
    {
        return $this->role?->name === 'guru';
    }

    public function isAdmin(): bool
    {
        return $this->role?->name === 'admin';
    }
}
