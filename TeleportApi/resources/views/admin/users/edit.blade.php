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
            <div class="row">
                <div class="col-sm-12 col-md-6">
                    <h3 class="content-heading pt-0">Имя</h3>
                    <p>{{ $user->name }}</p>
                </div>
                <div class="col-sm-12 col-md-6">
                    <h3 class="content-heading pt-0">Telegram</h3>
                    @if ($user->username)
                        <a href="https://t.me/{{ $user->username }}" target="_blank" class="link-effect">{{ $user->username }}</a>
                    @else
                        <span class="badge-pill badge-warning">Юзернейм отсутствует</span>
                    @endif
                </div>
            </div>
            <div class="row">
                <div class="col-sm-12 col-md-4">
                    <h3 class="content-heading pt-0">Текущий статус</h3>
                    <p>@if ($user->user_role == 'employer') <span class="badge-pill badge-info">Работодатель</span> @elseif($user->user_role == 'contractor') <span class="badge-pill badge-info">Соискатель</span> @endif</p>
                </div>
                <div class="col-sm-12 col-md-4">
                    <h3 class="content-heading pt-0">Баланс сосикателя</h3>
                    <p>{{ $user->balance_contractor }}</p>
                    <p>Тариф: <span class="badge-pill badge-info">
                            @if ($user->contractor_tariff == 'contractor_tariff_1')
                                Размещение 1-ого резюме
                            @elseif(($user->contractor_tariff == 'contractor_tariff_2'))
                                Размещение 2-х резюме
                            @elseif(($user->contractor_tariff == 'contractor_tariff_3'))
                                Размещение 3-х резюме
                            @else
                                Тариф не выбран
                            @endif
                        </span></p>
                </div>
                <div class="col-sm-12 col-md-4">
                    <h3 class="content-heading pt-0">Баланс работодателя</h3>
                    <p>{{ $user->balance_employer }}</p>
                    <p>Тариф: <span class="badge-pill badge-info">
                            @if ($user->employer_tariff == 'employer_tariff_1')
                                Размещение 1-ой вакансии
                            @elseif(($user->employer_tariff == 'employer_tariff_2'))
                                Размещение 2-х вакансий
                            @elseif(($user->employer_tariff == 'employer_tariff_3'))
                                Размещение 3-х вакансий
                            @else
                                Тариф не выбран
                            @endif
                        </span></p>
                </div>
            </div>
            <div class="row mb-50">
                <div class="col-sm-12 col-md-6">
                    <h3 class="content-heading">Резюме</h3>
                    <ul class="list-group list-group flush">
                        @foreach($user->resumes as $resume)
                            <a href="{{ route('admin.resumes.show', $resume->id) }}" class="link-effect list-group-item-action">{{ $resume->title }}</a>
                        @endforeach
                    </ul>
                </div>
                <div class="col-sm-12 col-md-6">
                    <h3 class="content-heading">Вакансии</h3>
                    <ul class="list-group list-group flush">
                        @foreach($user->vacations as $vacation)
                            <a href="{{ route('admin.vacations.show', $vacation->id) }}" class="link-effect list-group-item-action">{{ $vacation->title }}</a>
                        @endforeach
                    </ul>
                </div>
            </div>
        </div>
    </div>
    <form action="{{ route('admin.users.message', $user->id) }}" method="post">
        @csrf
        <div class="block">
            <div class="block-header block-header default">
                <div class="h3 block-title">Отправить сообщение</div>
                <div class="block-options">
                    <button class="btn btn-alt-success"><i class="fa fa-send mr-5"></i> Отправить</button>
                </div>
            </div>
            <div class="block-content">
                <div class="form-group">
                    <label for="text">Текст</label>
                    <textarea name="text" id="text" cols="30" rows="10" class="form-control"></textarea>
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
