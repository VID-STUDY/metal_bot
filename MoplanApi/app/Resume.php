<?php

namespace App;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Storage;

class Resume extends Model
{
    protected $fillable = [
        'title', 'price', 'name', 'contacts', 'location', 'user_id'
    ];

    /**
     * Resume owner
     *
     * @return \Illuminate\Database\Eloquent\Relations\HasOne
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    /**
     * Categories attached to resume
     *
     * @return \Illuminate\Database\Eloquent\Relations\BelongsToMany
     */
    public function categories()
    {
        return $this->belongsToMany(HandbookCategory::class, 'category_resume', 'resume_id', 'category_id');
    }

    public function getLocation()
    {
        $locations = json_decode(file_get_contents(Storage::path('locations.json')), true);
        if ($this->location == 'all')
            return '🗺 Вся Республика Узбекистан';
        $regionCode = explode('.', $this->location)[0];
        $cityCode = intval(explode('.', $this->location)[1]);
        $regionName = $locations["location.regions.$regionCode"];
        $cityName = $locations["location.regions.$regionCode.cities"][$cityCode];
        return "$regionName, $cityName";
    }
}
