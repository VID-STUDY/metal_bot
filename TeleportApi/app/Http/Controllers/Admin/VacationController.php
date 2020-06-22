<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
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
        $vacations = Vacation::all();
        return view('admin.vacations.index', compact('vacations'));
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Vacation  $vacation
     * @return \Illuminate\Http\Response
     */
    public function show(Vacation $vacation)
    {
        return view('admin.vacations.show', compact('vacation'));
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Vacation  $vacation
     * @return \Illuminate\Http\Response
     */
    public function destroy(Vacation $vacation)
    {
        $vacation->delete();
        return redirect()->route('admin.vacations.index');
    }
}
