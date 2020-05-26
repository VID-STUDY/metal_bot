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
        $vacation = Vacation::create($request->all());
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
        return $vacation;
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
        return response()->json($vacation, 200);
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
}
