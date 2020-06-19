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
}
