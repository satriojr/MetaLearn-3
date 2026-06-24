<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class UserProgress extends Model
{
    protected $fillable = ['user_id', 'mission_id', 'status', 'score', 'xp_earned', 'attempts', 'completed_at'];

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function mission()
    {
        return $this->belongsTo(Mission::class);
    }
}
