@extends('admin.layouts.app')

@section('title', $user->name . " - Статистика")

@section('css')
    <link rel="stylesheet" href="{{ asset('assets/js/plugins/bootstrap-datepicker/css/bootstrap-datepicker3.css') }}">
@endsection

@section('content')
    <div class="row js-appear-enabled animated fadeIn" data-toggle="appear">
        @isset($companiesCount)
            <div class="col-6">
                <a href="javascript:void(0)" class="block block-link-shadow text-center">
                    <div class="block-content block-content-full">
                        <div class="font-size-h3 font-w600">{{ $companiesCount }}</div>
                        <div class="font-size-sm font-w600 text-uppercase text-muted">Компаний за выбранный период</div>
                    </div>
                </a>
            </div>
        @endisset
        <div class="@if (isset($companiesCount)) col-6 @else col-12 @endif">
            <a href="javascript:void(0)" class="block block-link-shadow text-center">
                <div class="block-content block-content-full clearfix">
                    <div class="font-size-h3 font-w600">{{ $allCompaniesCount }}</div>
                    <div class="font-size-sm font-w600 text-uppercase text-muted">Компаний за весь период</div>
                </div>
            </a>
        </div>
    </div>
    <div class="row js-appear-enabled animated fadeIn" data-toggle="appear">
        <div class="col-12">
            <form action="" method="get">
                <div class="block">
                    <div class="block-header block-header-default">
                        <h3 class="block-title">Фильтр</h3>
                        <div class="block-options">
                            <button class="btn btn-alt-primary btn-sm" type="submit"><i class="fa fa-check"></i> Применить</button>
                            <a href="{{ route('admin.users.statistics', $user->id) }}" class="btn btn-alt-warning btn-sm"><i class="fa fa-refresh"></i> Сбросить</a>
                        </div>
                    </div>
                    <div class="block-content">
                        <div class="d-flex justify-content-center align-items-center mb-30">
                            <div class="input-daterange input-group js-datapicker-enabled" data-date-format="yyyy-mm-dd" data-week-start="1" data-autoclose="true" data-today-highlight="true">
                                <input type="date" name="start_date" id="start_date" class="form-control"
                                       placeholder="От" data-autoclose="true" data-today-highlight="true" @isset($startDate) value="{{ $startDate }}" @endisset>
                                <div class="px-30 d-flex align-items-center">
                                    <span class="input-group-text font-w600">До</span>
                                </div>
                                <input type="date" name="end_date" id="end_date" class="form-control"
                                       placeholder="До" data-autoclose="true" data-today-highlight="true" @isset($endDate) value="{{ $endDate }}" @endisset>
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
    <div class="block">
        <div class="block-header block-header-default">
            <h3 class="block-title">{{ $user->name }} <small>статистика</small></h3>
        </div>
        <div class="block-content block-content-full">
            <ul class="list-group list-group-flush mb-20">
                @foreach($history as $historyItem)
                    <li class="list-group-item d-flex justify-content-between align-items-center"><span>{!! $historyItem->getTitle() !!}</span>
                        <span class="badge badge-primary badge-pill">{{ $historyItem->created_at }}</span></li>
                @endforeach
            </ul>
            @if ($paginate)
                {{ $history->links('vendor.pagination.pagination') }}
            @endif
        </div>
    </div>
@endsection

@section('js')
    <script src="{{ asset('assets/js/plugins/bootstrap-datepicker/js/bootstrap-datepicker.js') }}"></script>
    <script src="{{ asset('assets/js/plugins/bootstrap-datepicker/locales/bootstrap-datepicker.ru.min.js') }}" charset="UTF-8"></script>
    <script>
        jQuery(function() {
            Codebase.helpers(['datepicker']);
        });
    </script>
@endsection
