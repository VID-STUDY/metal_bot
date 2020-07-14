<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class ReferralTender extends Model
{
    protected $fillable = [
        'date_from', 'date_to', 'ru_description', 'uz_description', 'total_pot'
    ];

    public function levels()
    {
        return $this->hasMany(ReferralTenderLevel::class);
    }

    public static function current()
    {
        $now = now()->format('Y-m-d');
        return self::where('date_from', '<=', $now)->where('date_to', '>=', $now)->first();
    }
}
