<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class LearningPath extends Model
{
    protected $fillable = ['topic_id', 'name', 'difficulty_level', 'description', 'sequence_order', 'is_active'];

    public function topic()
    {
        return $this->belongsTo(Topic::class);
    }

    public function missions()
    {
        return $this->hasMany(Mission::class);
    }
}
