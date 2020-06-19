<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Settings extends Model
{
    protected $fillable = [
        'employer_tariff_1', 'employer_tariff_2', 'employer_tariff_3',
        'contractor_tariff_1', 'contractor_tariff_2', 'contractor_tariff_3',
        'faq', 'about', 'partners', 'news'
    ];

    public static function get()
    {
        $settings = self::first();
        if (!$settings) {
            $settings = Settings::create(['employer_tariff_1' => 7000,
                'employer_tariff_2' => 13000, 'employer_tariff_3' => 18000, 'contractor_tariff_1' => 1200,
                'contractor_tariff_2' => 1100, 'contractor_tariff_3' => 1000]);
        }
        return $settings;
    }
}
