@extends('layouts.app')

@section('title', $vacation->title)

@section('content')
    <div class="block">
        <div class="block-header block-header-default">
            <h3 class="block-title">{{ $vacation->title }}</h3>
            <div class="block-options">
                <form action="{{ route('admin.vacations.destroy', $vacation->id) }}" method="post">
                    @csrf
                    @method('delete')
                    <button class="btn btn-alt-danger" onclick="return confirm('Вы уверены?')" data-toggle="tooltip" title="Удалить">
                        <i class="fa fa-trash mr-5"></i> Удалить</button>
                </form>
            </div>
        </div>
        <div class="block-content">
            <div class="row">
                <div class="col-md-4 col-sm-12">
                    <h3 class="content-heading">Цена</h3>
                    <p>{{ $vacation->price }}</p>
                </div>
                <div class="col-md-4 col-sm-12">
                    <h3 class="content-heading">Имя</h3>
                    <p>{{ $vacation->name }}</p>
                </div>
                <div class="col-md-4 col-sm-12">
                    <h3 class="content-heading">Контакты</h3>
                    <p><a href="callto:{{ $vacation->contacts}}" class="link-effect">{{ $vacation->contacts}}</a></p>
                </div>
                <div class="col-md-4 col-sm-12">
                    <h3 class="content-heading">Локация</h3>
                    <p>{{ $vacation->getLocation() }}</p>
                </div>
            </div>
            <div class="row mb-50">
                <div class="col-md-6 col-sm-12">
                    <h3 class="content-heading">Пользователь</h3>
                    <a href="{{ route('admin.users.edit', $vacation->user_id) }}" class="link-effect">{{ $vacation->user->name }}</a>
                </div>
                <div class="col-md-6 col-sm-12">
                    <h3 class="content-heading">Категории</h3>
                    <ul class="list-group list-group-flush">
                        @foreach($vacation->categories as $category)
                            <li class="list-group-item">{{ $category->ru_title }}</li>
                        @endforeach
                    </ul>
                </div>
            </div>
        </div>
    </div>
@endsection
