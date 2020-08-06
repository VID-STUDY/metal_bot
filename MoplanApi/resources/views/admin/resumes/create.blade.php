@extends('layouts.app')

@section('title', 'Создать закупку')

@section('css')
    <link rel="stylesheet" href="{{ asset('assets/js/plugins/select2/select2.min.css') }}">
    <link rel="stylesheet" href="{{ asset('assets/js/plugins/select2/select2-bootstrap.min.css') }}">
@endsection

@section('content')
    <form action="{{ route('admin.resumes.store') }}" method="post">
        @csrf
        <div class="block">
            <div class="block-header block-header-default">
                <h3 class="block-title">Создать закупку</h3>
                <div class="block-options">
                    <button class="btn btn-alt-success" type="submit"><i class="fa fa-check"></i> Сохранить</button>
                </div>
            </div>
            <div class="block-content">
                <div class="row">
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group">
                            <div class="form-material floating">
                                <input type="text" name="title" id="title" class="form-control" required>
                                <label for="title">Заголовок</label>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group">
                            <div class="form-material floating">
                                <input type="text" name="price" id="price" class="form-control" required>
                                <label for="price">Цена</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group">
                            <div class="form-material floating">
                                <input type="text" name="name" id="name" class="form-control" required>
                                <label for="name">Имя</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group">
                            <div class="form-material floating">
                                <input type="text" name="contacts" id="contacts" class="form-control" required>
                                <label for="contacts">Контакты</label>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group">
                            <div class="form-material floating">
                                <select name="location" id="location" class="form-control js-select2" required>
                                    <option value="all">🗺 Вся Республика Узбекистан</option>
                                    @foreach($locations as $region => $cities)
                                        <optgroup label="{{ $region }}">
                                            @foreach($cities as $city)
                                                <option value="{{ $loop->parent->index }}.{{ $loop->index }}">{{ $city }}</option>
                                            @endforeach
                                        </optgroup>
                                    @endforeach
                                </select>
                                <label for="location">Локация</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group">
                            <div class="form-material floating">
                                <select name="user_id" id="userId" class="form-control js-select2" required>
                                    @foreach($users as $user)
                                        <option value="{{ $user->id }}">{{ $user->name }}</option>
                                    @endforeach
                                </select>
                                <label for="userId">Пользователь</label>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group">
                            <div class="form-material floating">
                                <select name="categories[]" id="categories" class="form-control js-select2" required multiple>
                                    @foreach($categories as $category)
                                        <option value="{{ $category->id }}">{{ $category->ru_title }}</option>
                                    @endforeach
                                </select>
                                <label for="categories">Категории</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </form>
@endsection

@section('js')
    <script src="{{ asset('assets/js/plugins/select2/select2.full.min.js') }}"></script>
    <script>
        jQuery(function() {
            Codebase.helper('select2');
        });
    </script>
@endsection
