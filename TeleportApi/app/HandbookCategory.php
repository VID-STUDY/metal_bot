<?php

namespace App;

use Illuminate\Database\Eloquent\Model;
use Kalnoy\Nestedset\NodeTrait;

class HandbookCategory extends Model
{
    use NodeTrait;

    protected $fillable = [
        'ru_title', 'uz_title', 'parent_id', 'uz_description', 'ru_description'
    ];

    const UPLOAD_DIRECTORY = 'uploads/handbook_categories_images/';

    /**
     * Children categories
     *
     * @return \Illuminate\Database\Eloquent\Relations\HasMany
     */
    public function categories()
    {
        return $this->hasMany(self::class, 'parent_id', 'id');
    }

    /**
     * Check if category has children
     */
    public function hasCategories()
    {
        return $this->categories()->count() > 0;
    }

    /**
     * Parent category
     *
     * @return \Illuminate\Database\Eloquent\Relations\HasOne
     */
    public function parentCategory()
    {
        return $this->hasOne(self::class, 'id', 'parent_id');
    }

    /**
     * Check if category has parent category
     *
     * @return boolean
     */
    public function hasParentCategory()
    {
        return $this->parentCategory !== null;
    }


    /**
     * Override delete method to delete image too
     *
     * @return void
     * @throws \Exception
     */
    public function delete()
    {
        parent::delete();
    }

    /**
     * Get cleand title
     *
     * @return string
     */
    public function getTitle()
    {
        return strip_tags($this->ru_title);
    }

    public function vacations()
    {
        return $this->belongsToMany(Vacation::class, 'category_vacation', 'category_id', 'vacation_id');
    }

    public function resumes()
    {
        return $this->belongsToMany(Resume::class, 'category_resume', 'category_id', 'resume_id');
    }

}
