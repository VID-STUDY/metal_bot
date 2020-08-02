<?php

namespace App\Http\Controllers\Admin;

use App\HandbookCategory;
use App\Http\Controllers\Controller;
use App\Resume;
use App\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Storage;

class ResumeController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $resumes = Resume::all();
        return view('admin.resumes.index', compact('resumes'));
    }

    /**
     * Show create resume view
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
        return view('admin.resumes.create', compact('categories', 'users', 'locations'));
    }

    /**
     * Store a new resume
     *
     * @param Request $request
     * @return \Illuminate\Http\RedirectResponse
     */
    public function store(Request $request)
    {
        $data = $request->all();
        $resume = Resume::create($data);
        foreach ($data['categories'] as $category) {
            $resume->categories()->attach($category);
        }
        return redirect()->route('admin.resumes.index');
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Resume  $resume
     * @return \Illuminate\Http\Response
     */
    public function show(Resume $resume)
    {
        return view('admin.resumes.show', compact('resume'));
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param \App\Resume $resume
     * @return \Illuminate\Http\Response
     * @throws \Exception
     */
    public function destroy(Resume $resume)
    {
        $resume->delete();
        return redirect()->route('admin.resumes.index');
    }
}
