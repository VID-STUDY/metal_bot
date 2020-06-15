@extends('layouts.app')

@section('css')
    <link rel="stylesheet" href="{{ asset('assets/js/plugins/datatables/dataTables.bootstrap4.min.css') }}">
@endsection

@section('title') Категории @endsection

@section('content')
    <div class="block">
        <div class="block-header block-header-default">
            <h3 class="block-title">Справочник <small>Категории</small></h3>
            <div class="block-options">
                <a href="{{ route('admin.categories.create') }}" class="btn btn-alt-primary"><i
                        class="fa fa-plus mr-5"></i>Добавить категорию</a>
            </div>
        </div>
        <div class="block-content">
            <div class="table-responsive">
                <table class="table table-stripped table-bordered table-vcenter js-dataTable-full">
                    <thead>
                    <tr>
                        <th class="text-center">Заголовок</th>
                        <th class="text-center">Категории</th>
                        <th class="text-center" style="width: 15%">Действия</th>
                    </tr>
                    </thead>
                    <tbody>
                    @foreach($categories as $category)
                        <tr>
                            <td class="font-w600 text-center">{{ $category->getTitle() }}</td>
                            <td class="text-center">
                                @if($category->hasCategories())
                                    <a href="{{ route('admin.categories.show', $category->id) }}"
                                       class="btn btn-sm btn-alt-primary">Посмотреть</a>
                                @else
                                    Нет
                                @endif
                            </td>
                            <td class="text-center">
                                <div class="d-flex align-items-center h-100">
                                    <a href="{{ route('admin.categories.edit', $category->id) }}"
                                       data-toggle="tooltip" title="Редактировать" class="btn btn-sm btn-alt-info"><i
                                            class="fa fa-edit"></i></a>
                                    <form method="post"
                                          action="{{ route('admin.categories.destroy', $category->id) }}">
                                        @csrf
                                        @method('delete')
                                        <button style="border: none; cursor: pointer; background-color: transparent;"
                                                class="btn btn-sm btn-alt-danger"
                                                onclick="return confirm('Вы уверены?')" data-toggle="tooltip"
                                                title="Удалить">
                                            <i class="fa fa-trash"></i>
                                        </button>
                                    </form>
                                </div>
                            </td>
                        </tr>
                    @endforeach
                    </tbody>
                </table>
            </div>
        </div>
    </div>
@endsection

@section('js')
    <script src="{{ asset('assets/js/plugins/datatables/jquery.dataTables.min.js') }}"></script>
    <script src="{{ asset('assets/js/plugins/datatables/dataTables.bootstrap4.min.js') }}"></script>

    <script>
        jQuery('.js-dataTable-full').dataTable({
            "order": [],
            pageLength: 10,
            lengthMenu: [[10, 20, 30, 50], [10, 20, 30, 50]],
            autoWidth: true,
            language: ru_datatable
        });
    </script>
@endsection
