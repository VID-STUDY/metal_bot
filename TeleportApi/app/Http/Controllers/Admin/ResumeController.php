<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Resume;
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
