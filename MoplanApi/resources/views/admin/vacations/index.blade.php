@extends('layouts.app')

@section('title', 'Объявления')

@section('content')
    <div class="block">
        <div class="block-header block-header-default">
            <h3 class="block-title">Объявления</h3>
            <div class="block-options">
                <a href="{{ route('admin.vacations.create') }}" class="btn btn-alt-primary"><i
                        class="fa fa-plus mr-5"></i>Добавить объявление</a>
            </div>
        </div>
        <div class="block-content block-content-full">
            <div class="table-responsive">
                <table class="table table table-stripped table-bordered table-vcenter">
                    <thead>
                    <tr>
                        <th class="text-center">Заголовок</th>
                        <th class="text-center">Пользователь</th>
                        <th class="text-center">Действия</th>
                    </tr>
                    </thead>
                    <tbody>
                    @foreach($vacations as $vacation)
                        <tr>
                            <td class="text-center">{{ $vacation->title }}</td>
                            <td class="text-center">
                                @if ($vacation->user)
                                <a href="{{ route('admin.users.edit', $vacation->user_id) }}" class="link-effect">{{ $vacation->user->name }}</a>
                                @endif
                            </td>
                            <td class="d-flex justify-content-center align-items-center">
                                <a href="{{ route('admin.vacations.show', $vacation->id) }}" class="btn btn-sm btn-alt-info mr-10" data-toggle="tooltip" title="Посмотреть"><i class="fa fa-eye"></i></a>
                                <form action="{{ route('admin.vacations.destroy', $vacation->id) }}" method="post">
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
