<?php

namespace App\Http\Controllers;

use App\Vacation;
use App\Settings;
use Illuminate\Http\Request;

class VacationController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        return Vacation::all();
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $data = $request->all();
        $vacation = Vacation::create($data);
        foreach ($data['categories'] as $category) {
            $vacation->categories()->attach($category);
        }
        $user = $vacation->user;
        if ($user->free_actions_count > 0) {
            $user->free_actions_count -= 1;
        } else {
            $tariff = $user->employer_tariff;
            $vacationCost = Settings::get()->$tariff;
            $user->balance_employer -= $vacationCost;
        }
        $user->save();

        // Notify users about new vacation
        $resumes = collect();
        foreach ($vacation->categories as $category)
            $resumes = $resumes->merge($category->resumes);
        $resumes = $resumes->unique(function ($resume) {
            return $resume->id;
        });
        $resumes = $resumes->filter(function ($resume, $key) use ($user) {
            return $resume->user->id != $user->id;
        });
        if ($vacation->location !== 'all')
            $resumes = $resumes->filter(function ($resume, $key) use ($vacation) {
                return $resume->location == $vacation->location || $resume->location == 'all';
            });
        $users = $resumes->pluck('user');
        $users = $users->unique(function ($user) {
            return $user->id;
        });
        $result = [
            'vacation' => $vacation->load('user'),
            'notifyUsers' => $users
        ];


        return response()->json($result, 201);
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Vacation  $vacation
     * @return \Illuminate\Http\Response
     */
    public function show(Vacation $vacation)
    {
        return $vacation->load('categories');
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Vacation  $vacation
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Vacation $vacation)
    {
        $vacation->update($request->all());
        return response()->json($vacation->load('categories'), 200);
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param \App\Vacation $vacation
     * @return \Illuminate\Http\Response
     * @throws \Exception
     */
    public function destroy(Vacation $vacation)
    {
        $vacation->delete();

        return response()->json(null, 204);
    }

    /**
     * Get resumes that are suitable for vacation
     *
     * @param Vacation $vacation
     * @return \Illuminate\Http\Response
     */
    public function getResumesForVacation(Vacation $vacation)
    {
        $resumes = collect();
        foreach($vacation->categories as $category)
            $resumes = $resumes->merge($category->resumes);
        $resumes = $resumes->unique(function ($resume) {
            return $resume->id;
        })->filter(function ($resume, $key) use ($vacation) {
            return $resume->user->id != $vacation->user_id &&
                   !$resume->user->is_blocked;
        });
        if ($vacation->location !== 'all')
            $resumes = $resumes->filter(function ($resume, $key) use ($vacation) {
                return $resume->location == $vacation->location || $resume->location == 'all';
            });
        return $resumes;
    }
}
