<?php

namespace App\Http\Controllers;

use App\HandbookCategory;
use Illuminate\Http\Request;

class CategoryController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        return HandbookCategory::whereNull('parent_id')->get();
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\HandbookCategory  $category
     * @return \Illuminate\Http\Response
     */
    public function show(HandbookCategory $category)
    {
        return response()->json($category->load('categories')->load('vacations.user')->load('parentCategory'));
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\HandbookCategory  $handbookCategory
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, HandbookCategory $handbookCategory)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\HandbookCategory  $handbookCategory
     * @return \Illuminate\Http\Response
     */
    public function destroy(HandbookCategory $handbookCategory)
    {
        //
    }

    public function siblings(HandbookCategory $category)
    {
        return $category->siblingsAndSelf()->get();
    }
}
