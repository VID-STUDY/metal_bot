<?php


namespace App\Repositories;

interface HandbookCategoryRepositoryInterface
{
    /**
     * Get's a handbook category by it'id
     *
     * @param int $id
     * @return \App\HandbookCategory
    */
    public function get(int $id);

    /**
     * Get category by slug
     *
     * @param string $slug
     * @return \App\HandbookCategory
    */
    public function getBySlug(string $slug);

    /**
     * Gets all handbook categories
     *
     * @return mixed
    */
    public function all();

    /**
     * Get all categories without tree
     *
     * @return array
     */
    public function allWithoutTree();

    /**
     * Delete a handbook category
     *
     * @param int $id
     * @return int
    */
    public function delete(int $id);

    /**
     * Update a handbook category
     *
     * @param int $categoryId
     * @param object $categoryData
     * @return \App\HandbookCategory
    */
    public function update(int $categoryId, $categoryData);

    /**
     * Store a handbook category
     *
     * @param object $categoryData
     * @return \App\HandbookCategory
    */
    public function store($categoryData);

    /**
     * Get tree of handbook categories
     *
     * @return object
    */
    public function getTree();

    /**
     * Set position for category
     *
     * @param int $categoryId
     * @param int $position
     * @return bool
    */
    public function setPosition(int $categoryId, int $position);

    /**
     * Get favorites categories
     *
     * @return array
    */
    public function getFavoriteCategories();

    /**
     * Seacrh categories
     *
     * @param string $query
     * @param boolean $findOne
     * @return mixed
     */
    public function search(string $query, $findOne = false);
}
