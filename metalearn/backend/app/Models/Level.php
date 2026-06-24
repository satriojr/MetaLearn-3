<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Level extends Model
{
    protected $fillable = ['level_number', 'title', 'min_xp', 'max_xp', 'description'];

    public function userLevel()
    {
        return $this->hasMany(UserLevel::class);
    }
}
