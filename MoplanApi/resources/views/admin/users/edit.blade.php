@extends('layouts.app')

@section('title', 'Пользователь - '.$user->name)

@section('css')
    <link rel="stylesheet" href="{{ asset('assets/js/plugins/select2/select2.min.css') }}">
    <link rel="stylesheet" href="{{ asset('assets/js/plugins/select2/select2-bootstrap.min.css') }}">
@endsection

@section('content')
    <form action="{{ route('admin.users.update', $user->id) }}" method="post">
        @csrf
        @method('put')
        <div class="block">
            <div class="block-header block-header-default">
                <h3 class="block-title"><i class="fa fa-user-circle mr-5 text-muted"></i> {{ $user->name }} @if ($user->is_blocked) <small class="text-danger"><i class="si si-lock"></i> Заблокирован</small> @endif @if ($user->referralFrom) <small class="text-success"><i class="si si-user-follow"></i> Приглашён пользователем
                        <a href="{{ route('admin.users.edit', $user->referral_from_id) }}" class="link-effect">{{ $user->referralFrom->name }}</a></small>@endif</h3>
                <div class="block-options">
                    <a href="{{ route('admin.users.block', $user->id) }}" class="btn btn-alt-warning mr-5">@if ($user->is_blocked) <i class="si si-lock-open"></i> Разблокировать@else <i class="si si-lock"></i> Заблокировать@endif</a>
                    <button class="btn btn-alt-success"><i class="fa fa-check"></i> Сохранить</button>
                </div>
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
                            <a href="https://t.me/{{ $user->username }}" target="_blank"
                               class="link-effect">{{ $user->username }}</a>
                        @else
                            <span class="badge-pill badge-warning">Юзернейм отсутствует</span>
                        @endif
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-12 col-md-4">
                        <h3 class="content-heading pt-0">Текущий статус</h3>
                        <p>@if ($user->user_role == 'employer') <span
                                class="badge-pill badge-info">Продавец</span> @elseif($user->user_role == 'contractor')
                                <span class="badge-pill badge-info">Покупатель</span> @endif</p>
                    </div>
                    <div class="col-sm-12 col-md-4">
                        <h3 class="content-heading pt-0">Баланс покупателя</h3>
                        <div class="form-group">
                            <div class="form-material">
                                <input type="text" name="balance_contractor" id="balance_contractor" class="form-control"
                                       value="{{ $user->balance_contractor }}">
                            </div>
                        </div>
                        <div class="form-group">
                            <div class="form-material floating">
                                <select name="contractor_tariff" id="contractor_tariff" class="form-control">
                                    <option disabled>Тариф не выбран</option>
                                    <option value="contractor_tariff_1" @if ($user->contractor_tariff == 'contractor_tariff_1') selected @endif>Размещение 1-ого объявления</option>
                                    <option value="contractor_tariff_2" @if ($user->contractor_tariff == 'contractor_tariff_2') selected @endif>Размещение 2-х объявлений</option>
                                    <option value="contractor_tariff_3" @if ($user->contractor_tariff == 'contractor_tariff_3') selected @endif>Размещение 3-х объявлений</option>
                                </select>
                                <label for="contractor_tariff">Тариф</label>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-12 col-md-4">
                        <h3 class="content-heading pt-0">Баланс продавца</h3>
                        <div class="form-group">
                            <div class="form-material">
                                <input type="text" name="balance_employer" id="balance_employer" class="form-control"
                                       value="{{ $user->balance_employer }}">
                            </div>
                        </div>
                        <div class="form-group">
                            <div class="form-material floating">
                                <select name="employer_tariff" id="employer_tariff" class="form-control">
                                    <option disabled>Тариф не выбран</option>
                                    <option value="employer_tariff_1" @if ($user->employer_tariff == 'employer_tariff_1') selected @endif>Размещение 1-ого объявления</option>
                                    <option value="employer_tariff_2" @if ($user->employer_tariff == 'employer_tariff_2') selected @endif>Размещение 2-х объявлений</option>
                                    <option value="employer_tariff_3" @if ($user->employer_tariff == 'employer_tariff_3') selected @endif>Размещение 3-х объявлений</option>
                                </select>
                                <label for="employer_tariff">Тариф</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row mb-50">
                    <div class="col-sm-12 col-md-6">
                        <h3 class="content-heading">Закупки</h3>
                        <ul class="list-group list-group flush">
                            @foreach($user->resumes as $resume)
                                <a href="{{ route('admin.resumes.show', $resume->id) }}"
                                   class="link-effect list-group-item-action mt-10">{{ $resume->title }}</a>
                            @endforeach
                        </ul>
                    </div>
                    <div class="col-sm-12 col-md-6">
                        <h3 class="content-heading">Объявления на продажу</h3>
                        <ul class="list-group list-group flush">
                            @foreach($user->vacations as $vacation)
                                <a href="{{ route('admin.vacations.show', $vacation->id) }}"
                                   class="link-effect list-group-item-action mt-10">{{ $vacation->title }}</a>
                            @endforeach
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </form>
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
    <h2 class="content-heading">Статистика</h2>
    <div class="block">
        <div class="block-header block-header-default">
            <h3 class="block-title">
                @if ($referralTender)
                    <i class="si si-user-follow mr-5"></i>Пользователи, приглаёшнные по реферальной ссылки в течении текущего конкурса {{ $referralTender->date_from }} - {{ $referralTender->date_to }} <span class="badge badge-pill badge-primary">{{ $referralsInTender->count() }}</span>
                @else
                    <i class="si si-user-follow mr-5"></i>Пользователи, приглашённые за всё время в условиях всех реферальных конкурсов <span class="badge badge-pill badge-primary">{{ $referralsInTender->count() }}</span>
                @endif
            </h3>
        </div>
        <div class="block-content block-content-full">
            <ul class="list-group list-group-flush mb-20">
                @foreach($referralsInTender as $referral)
                    <li class="list-group-item">
                        <a href="{{ route('admin.users.edit', $referral->id) }}" class="link-effect">{{ $referral->name }}</a>
                    </li>
                @endforeach
            </ul>
        </div>
    </div>
    <div class="block">
        <div class="block-header block-header-default">
            <h3 class="block-title"><i class="si si-user-follow mr-5"></i>Пользователи, приглашённые вне условий реферальных конкурсов <span class="badge badge-pill badge-primary">{{ $referralsNotInTender->count() }}</span></h3>
        </div>
        <div class="block-content block-content-full">
            <ul class="list-group list-group-flush mb-20">
                @foreach($referralsNotInTender as $referral)
                    <li class="list-group-item">
                        <a href="{{ route('admin.users.edit', $referral->id) }}" class="link-effect">{{ $referral->name }}</a>
                    </li>
                @endforeach
            </ul>
        </div>
    </div>
@endsection
@section('js')
    <script src="{{ asset('assets/js/plugins/select2/select2.full.min.js') }}"></script>
    <script>
        jQuery(function () {
            Codebase.helper('select2');
        });
    </script>
@endsection
