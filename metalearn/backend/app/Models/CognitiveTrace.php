<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class CognitiveTrace extends Model
{
    public $timestamps = false;

    protected $fillable = ['user_id', 'question_id', 'action_type', 'duration_ms', 'payload', 'recorded_at'];

    protected function casts(): array
    {
        return [
            'payload' => 'array',
            'recorded_at' => 'datetime',
        ];
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function question()
    {
        return $this->belongsTo(Question::class, 'question_id');
    }
}
