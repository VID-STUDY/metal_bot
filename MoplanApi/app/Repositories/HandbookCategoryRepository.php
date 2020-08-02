<?php


namespace App\Repositories;

use App\HandbookCategory;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;


class HandbookCategoryRepository implements HandbookCategoryRepositoryInterface
{

    /**
     * Get's a handbook category by it'id
     *
     * @param int $id
     * @return \App\Models\HandbookCategory
     */
    public function get(int $id)
    {
        return HandbookCategory::find($id);
    }

    /**
     * Gets all handbook categories
     *
     * @return mixed
     */
    public function all()
    {
        return HandbookCategory::where('parent_id', null)->orderBy('position', 'asc')->get();
    }

    /**
     * Get all categories without tree
     *
     * @return array
     */
    public function allWithoutTree()
    {
        return HandbookCategory::all();
    }

    /**
     * Delete a handbook category
     *
     * @param int $id
     * @return int
     * @throws \Exception
     */
    public function delete(int $id)
    {
        $category = $this->get($id);
        $parentId = $category->getParentId();
        $category->delete();
        return $parentId;
    }

    /**
     * Update a handbook category
     *
     * @param int $categoryId
     * @param \Illuminate\Http\Request $categoryData
     * @return \App\Models\HandbookCategory
     */
    public function update(int $categoryId, $categoryData)
    {
        $category = $this->get($categoryId);
        $category->update($categoryData->all());

        return $category;
    }

    /**
     * Store a handbook category
     *
     * @param \Illuminate\Http\Request $categoryData
     * @return \App\Models\HandbookCategory
     */
    public function store($categoryData)
    {
        $category = HandbookCategory::create($categoryData->all());

        $parentId = $categoryData->get('parent_id');

        if ($parentId != 0)
        {
            $parent = $this->get($parentId);
            $category->appendToNode($parent)->save();
        }

        return $category;
    }

    /**
     * Get tree of handbook categories
     *
     * @return object
     */
    public function getTree()
    {
        return HandbookCategory::all()->toTree();
    }

    /**
     * Set position for category
     *
     * @param int $categoryId
     * @param int $position
     * @return bool
     */
    public function setPosition(int $categoryId, int $position)
    {
        $category = $this->get($categoryId);
        $category->position = $position;
        return $category->save();
    }

    /**
     * Get favorites categories
     *
     * @return array
     */
    public function getFavoriteCategories()
    {
        return HandbookCategory::where('favorite', true)->orderBy('position', 'asc')->get();
    }

    /**
     * Seacrh categories
     *
     * @param string $query
     * @param boolean $findOne
     * @return mixed
     */
    public function search(string $query, $findOne = false)
    {
        if ($findOne)
            return HandbookCategory::where('ru_title', $query)->first();
        else
            return HandbookCategory::where('ru_title', 'like', "%$query%")->get();
    }

    /**
     * Get category by slug
     *
     * @param string $slug
     * @return \App\Models\HandbookCategory
     */
    public function getBySlug(string $slug)
    {
        $category = HandbookCategory::where('ru_slug', $slug)->first();
        return $category;
    }
}
