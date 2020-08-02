<?php

namespace App\Http\Controllers\Admin;

use App\HandbookCategory;
use App\Http\Controllers\Controller;
use App\User;
use App\Vacation;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

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
     * Show create vacation view
     *
     * @return \Illuminate\Contracts\View\Factory|\Illuminate\View\View
     */
    public function create()
    {
        $categories = HandbookCategory::all();
        $categories = $categories->filter(function ($category, $key) {
            return !$category->hasCategories();
        });
        $users = User::where('name', '!=', 'Admin')->get();
        $rawLocations = json_decode(file_get_contents(Storage::path('locations.json')), true);
        $locations = array();
        foreach ($rawLocations as $key => $region)
        {
            try {
                $cities = $rawLocations[$key . '.cities'];
            } catch (\ErrorException $exception) {
                continue;
            }
            $locations[$region] = $cities;
        }
        return view('admin.vacations.create', compact('categories', 'users', 'locations'));
    }

    /**
     * Store a new vacation
     *
     * @param Request $request
     * @return \Illuminate\Http\RedirectResponse
     */
    public function store(Request $request)
    {
        $data = $request->all();
        $vacation = Vacation::create($data);
        foreach ($data['categories'] as $category) {
            $vacation->categories()->attach($category);
        }
        return redirect()->route('admin.vacations.index');
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
