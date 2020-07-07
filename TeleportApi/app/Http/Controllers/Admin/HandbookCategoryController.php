<?php

namespace App\Http\Controllers\Admin;

use App\Repositories\HandbookCategoryRepositoryInterface;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;
use Illuminate\Http\Response;
use Illuminate\Support\Facades\Storage;

class HandbookCategoryController extends Controller
{
    /**
     * HandbookCategory repository
     *
     * @var HandbookCategoryRepositoryInterface
    */
    protected $handbookCategoryRepository;

    /**
     * Create a new instance
     *
     * @param HandbookCategoryRepositoryInterface $handbookCategoryRepository
     * @return void
    */
    public function __construct(HandbookCategoryRepositoryInterface $handbookCategoryRepository)
    {
        $this->handbookCategoryRepository = $handbookCategoryRepository;
    }

    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $data = [
            'categories' => $this->handbookCategoryRepository->all()
        ];

        return view('admin.categories.index', $data);
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        $data = [
            'categories' => $this->handbookCategoryRepository->getTree(),
        ];

        return view('admin.categories.create', $data);
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $request->validate([
            'ru_title' => 'required|max:255',
        ]);

        $category = $this->handbookCategoryRepository->store($request);
        if ($request->has('saveQuit'))
        {
            $parent = $category->getParentId();
            if ($parent != null)
                return redirect()->route('admin.categories.show', $parent);
            else
                return redirect()->route('admin.categories.index');
        }
        else
            return redirect()->route('admin.categories.create');
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        $data = [
            'category' => $this->handbookCategoryRepository->get($id)
        ];

        return view('admin.categories.category', $data);
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function edit($id)
    {
        $data = [
            'category' => $this->handbookCategoryRepository->get($id),
            'categories' => $this->handbookCategoryRepository->getTree()
        ];
        return view('admin.categories.edit', $data);
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        $request->validate([
            'ru_title' => 'required|max:255',
        ]);
        $category = $this->handbookCategoryRepository->update($id, $request);

        $parentId = $category->getParentId();
        if ($parentId != null)
            return redirect()->route('admin.categories.show', $parentId);
        else
            return redirect()->route('admin.categories.index');
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        $parent = $this->handbookCategoryRepository->delete($id);

        if ($parent != null && $this->handbookCategoryRepository->get($parent)->hasCategories())
            return redirect()->route('admin.categories.show', $parent);
        else
            return redirect()->route('admin.categories.index');
    }

    /**
     * Change position for category
     *
     * @param Request $request
     * @return \Symfony\Component\HttpFoundation\Response
     */
    public function changePosition(Request $request)
    {
        $categoryId = $request->get('id');
        $position = $request->get('position');
        if ($this->handbookCategoryRepository->setPosition($categoryId, $position))
            return Response::create("", 200);
        else
            return Response::create("", 400);
    }
}
