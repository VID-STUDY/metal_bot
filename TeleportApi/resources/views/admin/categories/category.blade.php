@extends('layouts.app')

@section('css')
    <link rel="stylesheet" href="{{ asset('assets/js/plugins/datatables/dataTables.bootstrap4.min.css') }}">
@endsection

@section('title'){{ $category->ru_title }} @endsection

@section('content')
    <div class="block">
        <div class="block-header block-header-default">
            <h3 class="block-title">Категории</h3>
            <div class="block-options">
                <a href="{{ route('admin.categories.create') }}" class="btn btn-alt-primary"><i class="fa fa-plus mr-5"></i>Добавить</a>
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
                    @foreach($category->categories()->orderBy('position', 'asc')->get() as $childCategory)
                        <tr>
                            <td class="font-w600">{{ $childCategory->getTitle() }}</td>
                            <td class="text-center">
                                @if($childCategory->hasCategories())
                                    <a href="{{ route('admin.categories.show', $childCategory->id) }}" class="btn btn-sm btn-alt-primary">Посмотреть</a>
                                @else
                                    Нет
                                @endif
                            </td>
                            <td class="text-center">
                                <div class="d-flex align-items-center justify-content-around">
                                    <a href="{{ route('admin.categories.edit', $childCategory->id) }}" data-toggle="tooltip" class="btn btn-sm btn-alt-info" title="Редактировать"><i class="fa fa-edit"></i></a>
                                    <form method="post" action="{{ route('admin.categories.destroy', $childCategory->id) }}">
                                        @csrf
                                        @method('delete')
                                        <button class="btn btn-sm btn-alt-danger" onclick="return confirm('Вы уверены?')" data-toggle="tooltip" title="Удалить">
                                            <i class="fa fa-trash"></i>
                                        </button>
                                    </form>
                                    <select name="position" class="position" data-id="{{ $childCategory->id }}">
                                        @for($i = 1; $i <= $category->categories->count(); $i++)
                                            <option value="{{ $i }}"
                                                    @if($childCategory->position == $i) selected @endif>{{ $i }}</option>
                                        @endfor
                                    </select>
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
        $('.position').change(function () {
            $.ajaxSetup({
                headers: {
                    'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
                }
            });
            let formData = new FormData;
            formData.append('id', $(this).data('id'));
            formData.append('position', $(this).val());
            $.ajax({
                type: 'POST',
                url: '{{ route('admin.categories.change.position') }}',
                dataType: 'json',
                data: formData,
                processData: false,
                contentType: false,
                beforeSend: function () {
                    $('.position').attr('disabled', 'disabled');
                },
                success: function () {
                    $('.position').removeAttr('disabled', '');
                },
                error: function (data) {
                    console.log(data);
                    $('.position').removeAttr('disabled', '');
                }
            })
        });
    </script>
@endsection
