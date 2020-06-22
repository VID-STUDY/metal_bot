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

Route::middleware('auth')->name('admin.')->namespace('Admin')->group(function () {
    // Dashboard
    Route::get('/', 'DashboardController@index')->name('index');
    // Handbook Category Routes
    Route::resource('/categories', 'HandbookCategoryController');

    // Users routes
    Route::resource('/users', 'UserController');
    Route::post('/users/{userId}/message', 'UserController@sendMessage')->name('users.message');

    Route::resource('/referral', 'ReferralController');

    Route::resource('/settings', 'SettingsController');

    Route::get('/telegram', 'TelegramController@index')->name('telegram.index');
    Route::post('/telegram/distribution', 'TelegramController@distribution')->name('telegram.distribution');

    Route::resource('resumes', 'ResumeController');

    Route::resource('vacations', 'VacationController');
});

Route::prefix('api')->group(function () {
    Route::apiResource('users', 'UsersController');
    Route::get('/users/{user}/resumes', "UsersController@getResumes");
    Route::get('/users/{user}/vacations', 'UsersController@getVacations');

    Route::apiResource('vacations', 'VacationController');
    Route::get('/vacations/{vacation}/resumes', 'VacationController@getResumesForVacation');

    Route::apiResource('categories', 'CategoryController');
    Route::get('/categories/{category}/siblings', 'CategoryController@siblings');

    Route::apiResource('resumes', 'ResumeController');
    Route::get('/resumes/{resume}/vacations', 'ResumeController@getVacationsForResume');

    Route::get('referral/current', 'ReferralController@current');
    Route::get('referral/invited', 'ReferralController@invited');
    Route::apiResource('referral', 'ReferralController');
    Route::get('referral/{referralTenderId}/top', 'ReferralController@topReferrals');

    Route::get('/settings', 'SettingsController@index');
});

Auth::routes();

Route::get('/home', 'HomeController@index')->name('home');
