<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class UserLevel extends Model
{
    public $timestamps = false;
    protected $table = 'user_level';

    protected $fillable = ['user_id', 'current_xp', 'level_id'];

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function level()
    {
        return $this->belongsTo(Level::class);
    }
}

