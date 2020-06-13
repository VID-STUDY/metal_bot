<?php

namespace App\Http\Controllers;

use App\Vacation;
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
        return response()->json($vacation, 201);
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
        $resumes = $resumes->unique(function ($item) {
            return $item->id;
        });
        if ($vacation->location !== 'all')
            $resumes = $resumes->filter(function ($resume, $key) use ($vacation) {
                return $resume->location == $vacation->location || $resume->location == 'all';
            });
        return $resumes;
    }
}
