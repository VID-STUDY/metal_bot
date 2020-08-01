@extends('layouts.app')

@section('title', 'Telegram')

@section('content')
    <form action="{{ route('admin.telegram.distribution') }}" method="post" enctype="multipart/form-data">
        @csrf
        <div class="block">
            <div class="block-header block-header-default">
                <h3 class="block-title">Рассылка</h3>
                <div class="block-options">
                    <button class="btn btn-alt-success" type="submit"><i class="fa fa-send mr-5"></i> Отправить</button>
                </div>
            </div>
            <div class="block-content">
                <div class="form-group">
                    <label for="text">Текст</label>
                    <textarea name="text" id="text" cols="30" rows="10" class="form-control"></textarea>
                </div>
                <div class="form-group">
                    <label for="image">Файл (Изображение \ Видео)</label> <br>
                    <input type="file" name="image" id="image">
                </div>
            </div>
        </div>
    </form>
@endsection
