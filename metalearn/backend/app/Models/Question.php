<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Question extends Model
{
    protected $table = 'question_bank';

    protected $fillable = ['mission_id', 'type', 'question_text', 'correct_answer', 'explanation', 'structure_answer', 'xp_value'];

    public function mission()
    {
        return $this->belongsTo(Mission::class);
    }

    public function options()
    {
        return $this->hasMany(AnswerOption::class, 'question_id');
    }

    public function cognitiveTraces()
    {
        return $this->hasMany(CognitiveTrace::class, 'question_id');
    }
}
