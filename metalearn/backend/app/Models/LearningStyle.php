<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class LearningStyle extends Model
{
    protected $fillable = ['code', 'name', 'description'];

    public function users()
    {
        return $this->hasMany(User::class);
    }
}
