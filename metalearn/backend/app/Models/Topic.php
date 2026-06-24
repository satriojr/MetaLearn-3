<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Topic extends Model
{
    protected $fillable = ['name', 'description', 'icon', 'color_hex', 'category'];

    public function learningPaths()
    {
        return $this->hasMany(LearningPath::class);
    }
}
