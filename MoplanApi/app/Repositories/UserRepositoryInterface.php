<?php


namespace App\Repositories;


use App\User;
use Illuminate\Database\Eloquent\Collection;

interface UserRepositoryInterface
{
    /**
     * Get all users
     *
     * @return mixed
    */
    public function all();

    /**
     * Get user by it's id
     *
     * @param int $userId
     * @return User
    */
    public function get($userId);

    /**
     * Create an User
     *
     * @param \Illuminate\Http\Request $userData
     * @param int $userRoleId
     * @return void
    */
    public function create($userData);

    /**
     * Update an user
     *
     * @param int $userId
     * @param \Illuminate\Http\Request $userData
     * @return void
    */
    public function update($userId, $userData);

    /**
     * Delete user
     *
     * @param int $userId
     * @return void
    */
    public function delete($userId);
}
