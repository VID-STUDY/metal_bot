@extends('layouts.app')

@section('title', 'Пользователь - '.$user->name)

@section('css')
    <link rel="stylesheet" href="{{ asset('assets/js/plugins/select2/select2.min.css') }}">
    <link rel="stylesheet" href="{{ asset('assets/js/plugins/select2/select2-bootstrap.min.css') }}">
@endsection

@section('content')

    <div class="block">
        <div class="block-header block-header-default">
            <h3 class="block-title"><i class="fa fa-user-circle mr-5 text-muted"></i> {{ $user->name }}</h3>
        </div>
        <div class="block-content">
            <form action="{{ route('admin.users.update', $user->id) }}" method="post" enctype="multipart/form-data">
                @csrf
                @method('put')
                <div class="row">
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group @error('name') is-invalid @enderror">
                            <div class="form-material floating">
                                <input type="text" name="name" id="name" value="{{ $user->name }}" class="form-control">
                                <label for="name">Имя пользователя</label>
                            </div>
                            @error('name') <div class="invalid-feedback animated fadeInDown">{{ $message }}</div> @enderror
                        </div>
                    </div>
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group @error('email') is-invalid @enderror">
                            <div class="form-material floating">
                                <input type="email" name="email" id="email" class="form-control" value="{{ $user->email }}">
                                <label for="email">Email</label>
                            </div>
                            @error('email') <div class="invalid-feedback animated fadeInDown">{{ $message }}</div> @enderror
                        </div>
                    </div>
                </div>
                <div class="block-content mb-10">
                    <div class="block-content text-right pb-10">
                        <button class="btn btn-alt-success" type="submit">Сохранить</button>
                    </div>
                </div>
            </form>
        </div>
    </div>


{{--    <a href="{{ route('admin.users.statistics', $user->id) }}" class="block block-link-shadow">--}}
{{--        <div class="block-content block-content-full my-50">--}}
{{--            <div class="font-size-h3 font-w600 text-center">Посмотреть статистику действий</div>--}}
{{--        </div>--}}
{{--    </a>--}}
@endsection
@section('js')
    <script src="{{ asset('assets/js/plugins/select2/select2.full.min.js') }}"></script>
    <script>
        jQuery(function() {
            Codebase.helper('select2');
        });
    </script>
@endsection
