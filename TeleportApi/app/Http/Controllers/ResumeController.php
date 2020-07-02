<?php

namespace App\Http\Controllers;

use App\Resume;
use App\Settings;
use Illuminate\Http\Request;

class ResumeController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        return Resume::all();
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
        $resume = Resume::create($data);
        foreach ($data['categories'] as $category) {
            $resume->categories()->attach($category);
        }
        $user = $resume->user;
        if ($user->free_actions_count > 0) {
            $user->free_actions_count -= 1;
        } else {
            $tariff = $user->contractor_tariff;
            $resumeCost = Settings::get()->$tariff;
            $user->balance_contractor -= $resumeCost;
        }
        $user->save();
        $vacations = collect();
        foreach($resume->categories as $category) {
            $vacations = $vacations->merge($category->vacations);
        }
        $vacations = $vacations->unique(function ($item) {
            return $item->id;
        })->filter(function ($vacation, $key) use ($user) {
            return $vacation->user->id != $user->id;
        });
        if ($resume->location !== 'all')
            $vacations = $vacations->filter(function ($vacation, $key) use ($resume) {
                return $vacation->location == $resume->location || $vacation->location == 'all';
            });
        $users = $vacations->pluck('user');
        $users = $users->unique(function ($user) {
            return $user->id;
        });
        $result = [
            'resume' => $resume->load('user'),
            'notifyUsers' => $users
        ];
        return response()->json($result, 201);
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Resume  $resume
     * @return \Illuminate\Http\Response
     */
    public function show(Resume $resume)
    {
        return $resume->load('categories');
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Resume  $resume
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Resume $resume)
    {
        $resume->update($request->all());
        return response()->json($resume->load('categories'), 200);
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Resume  $resume
     * @return \Illuminate\Http\Response
     */
    public function destroy(Resume $resume)
    {
        $resume->delete();

        return response()->json(null, 204);
    }

    /**
     * Get vacations that are suitable for resume
     *
     * @param Resume $resume
     * @return \Illuminate\Http\Response
     */
    public function getVacationsForResume(Resume $resume)
    {
        $vacations = collect();
        foreach($resume->categories as $category) {
            $vacations = $vacations->merge($category->vacations);
        }
        $vacations = $vacations->unique(function ($item) {
            return $item->id;
        });
        $vacations = $vacations->filter(function ($vacation, $key) use ($resume) {
            return $vacation->user->id != $resume->user_id &&
                   !$vacation->user->is_blocked;
        });
        if ($resume->location !== 'all')
            $vacations = $vacations->filter(function ($vacation, $key) use ($resume) {
                return $vacation->location == $resume->location || $vacation->location == 'all';
            });
        return $vacations;
    }
}
