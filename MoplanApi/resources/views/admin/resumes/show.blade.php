@extends('layouts.app')

@section('title', $resume->title)

@section('content')
    <div class="block">
        <div class="block-header block-header-default">
            <h3 class="block-title">{{ $resume->title }}</h3>
            <div class="block-options">
                <form action="{{ route('admin.resumes.destroy', $resume->id) }}" method="post">
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
                    <h3 class="content-heading">Описание</h3>
                    <p>{{ $resume->description }}</p>
                </div>
                <div class="col-md-4 col-sm-12">
                    <h3 class="content-heading">Контакты</h3>
                    <p>{{ $resume->contacts }}</p>
                </div>
                <div class="col-md-4 col-sm-12">
                    <h3 class="content-heading">Локация</h3>
                    <p>{{ $resume->getLocation() }}</p>
                </div>
            </div>
            <div class="row mb-50">
                <div class="col-md-6 col-sm-12">
                    <h3 class="content-heading">Пользователь</h3>
                    <a href="{{ route('admin.users.edit', $resume->user_id) }}" class="link-effect">{{ $resume->user->name }}</a>
                </div>
                <div class="col-md-6 col-sm-12">
                    <h3 class="content-heading">Категории</h3>
                    <ul class="list-group list-group-flush">
                        @foreach($resume->categories as $category)
                            <li class="list-group-item">{{ $category->ru_title }}</li>
                        @endforeach
                    </ul>
                </div>
            </div>
        </div>
    </div>
@endsection
