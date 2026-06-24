<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Mission extends Model
{
    protected $fillable = ['learning_path_id', 'title', 'type', 'difficulty', 'xp_reward', 'estimated_minutes', 'sequence_order'];

    public function learningPath()
    {
        return $this->belongsTo(LearningPath::class);
    }

    public function questions()
    {
        return $this->hasMany(Question::class);
    }

    public function progress()
    {
        return $this->hasMany(UserProgress::class);
    }
}
