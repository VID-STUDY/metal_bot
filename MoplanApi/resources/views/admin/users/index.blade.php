@extends('layouts.app')

@section('title', 'Пользователи')

@section('css')
    <link rel="stylesheet" href="{{ asset('assets/js/plugins/datatables/dataTables.bootstrap4.min.css') }}">

    <style>
        .js-dataTable-full .btn {
            height: 100%;
        }
    </style>
@endsection

@section('content')
    <div class="block">
        <div class="block-header block-header-default">
            <h3 class="block-title">Пользователи</h3>
            <div class="block-options">
                <a href="{{route('admin.users.create')}}" class="btn btn-alt-success"><i class="fa fa-plus mr-5"></i> Создать</a>
            </div>
        </div>
        <div class="block-content block-content-full">
            <div class="table-responsive">
                <table class="table table-stripped table-bordered table-vcenter js-dataTable-full">
                    <thead>
                    <tr>
                        <th class="text-center">Имя</th>
                        <th class="text-center">Роль</th>
                        <th class="text-center">Создан</th>
                        <th class="text-center">Действия</th>
                    </tr>
                    </thead>
                    <tbody>
                        @foreach($users as $user)
                            <tr>
                                <td class="text-center font-w600">{{ $user->name }} @if ($user->is_blocked) <small class="text-danger"><i class="si si-lock"></i> Заблокирован</small> @endif</td>
                                <td class="text-center font-w600"><span class="badge badge-pill badge-primary">@if ($user->user_role == 'contractor')Покупатель@elseif($user->user_role=='employer')Продавец@endif</span></td>
                                <td class="text-center font-w600">{{ $user->created_at->format('d.m.Y h:i:s') }}</td>
                                <td class="text-center font-w600 d-flex align-items-center justify-content-center">
                                    <a href="{{ route('admin.users.edit', $user->id) }}" class="btn btn-sm btn-alt-info mr-10" data-toggle="tooltip"
                                       title="Редактировать"><i class="fa fa-edit"></i></a>
                                    <form action="{{ route('admin.users.destroy', $user->id) }}" method="post">
                                        @csrf
                                        @method('delete')
                                        <button class="btn btn-sm btn-alt-danger" onclick="return confirm('Вы уверены?')" data-toggle="tooltip" title="Удалить">
                                            <i class="fa fa-trash"></i></button>
                                    </form>
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
