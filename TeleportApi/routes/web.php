<?php

use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () {
    return view('welcome');
});

Route::prefix('api')->group(function () {
    Route::apiResource('users', 'UsersController');
    Route::get('/users/{user}/getResumes', "UsersController@getResumes");

    Route::apiResource('vacations', 'VacationController');

    Route::apiResource('categories', 'CategoryController');
    Route::get('/categories/{category}/siblings', 'CategoryController@siblings');

    Route::apiResource('resumes', 'ResumeController');
});
