@extends('layouts.app')

@section('title', $referral->date_from. '-'. $referral->date_to)

@section('content')
    <form action="{{ route('admin.referral.update', $referral->id) }}" method="post">
        @method('put')
        <div class="block">
            <div class="block-header block-header-default">
                <h3 class="block-title">Редактировать реферальный конкурс {{ $referral->date_from. '-'. $referral->date_to }}</h3>
                <div class="block-options">
                    <button type="submit" class="btn btn-alt-success"><i class="fa fa-check"></i> Сохранить</button>
                </div>
            </div>
            <div class="block-content">
                @csrf
                <div class="row">
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group">
                            <label for="date_from">Дата начала/конца</label>
                            <div class="input-daterange input-group js-datepicker" data-date-format="yyyy-mm-dd"
                                 data-week-start="1" data-today-highlight="true">
                                <input type="text" name="date_from" id="date_from" placeholder="Начало"
                                       class="form-control" value="{{ $referral->date_from }}">
                                <input type="text" name="date_to" id="date_to" class="form-control" placeholder="Конец" value="{{ $referral->date_to }}">
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group @error('total_pot')is-invalid @enderror">
                            <div class="form-material floating">
                                <input type="number" name="total_pot" id="total_pot" class="form-control" value="{{ $referral->total_pot }}">
                                <label for="total_pot">Общий банк (только число)</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group @error('ru_description')is-invalid @enderror">
                            <label for="ru_description">Описание RU</label>
                            <textarea name="ru_description" id="ru_description"
                                      class="form-control">
                                {!! $referral->ru_description !!}
                            </textarea>
                        </div>
                    </div>
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group @error('uz_description')is-invalid @enderror">
                            <label for="uz_description">Описание UZ</label>
                            <textarea name="uz_description" id="uz_description"
                                      class="form-control">
                                {!! $referral->uz_description !!}
                            </textarea>
                        </div>
                    </div>
                </div>
                <div class="d-flex align-items-center justify-content-between   ">
                    <h2 class="content-heading">Уровни</h2>
                    <button class="btn btn-alt-info btn-primary" id="addLevelButton" type="button"><i
                            class="fa fa-plus"></i> Добавить
                    </button>
                </div>
                <div id="levels">
                    @foreach($referral->levels as $key => $level)
                        <div class="referral-level mt-20" style="border-bottom: 1px solid #eaecee;" id="referralLevel{{ $key }}">
                            <div class="d-flex align-items-center justify-content-between">
                                <h3 class="font-w600">Уровень</h3>
                                <button class="btn btn-small btn-alt-danger btn-sm btn-rounded delete-button" type="button"
                                        data-id="referralLevel{{ $key }}" data-toggle="tooltip" title="Удалить"><i class="si si-trash"></i>
                                </button>
                            </div>
                            <label for="users_from{{ $key }}">Количество пользователей, которое необходимо набрать</label>
                            <div class="row">
                                <div class="col-sm-12 col-md-6">
                                    <div class="form-group">
                                        <div class="form-material">
                                            <input type="number" name="levels[{{ $key }}][users_from]" id="users_from{{ $key }}" placeholder="От"
                                                   class="form-control" value="{{ $level->users_from }}">
                                        </div>
                                    </div>
                                </div>
                                <div class="col-sm-12 col-md-6">
                                    <div class="form-group">
                                        <div class="form-material">
                                            <input type="number" name="levels[{{ $key }}][users_to]" id="users_to{{ $key }}" placeholder="До"
                                                   class="form-control" value="{{ $level->users_to }}">
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-12 col-md-6">
                                    <div class="form-group">
                                        <div class="form-material floating">
                                            <input type="text" name="levels[{{ $key }}][ru_reward]" value="{{ $level->ru_reward }}" id="ru_reward{{ $key }}" class="form-control">
                                            <label for="ru_reward{{ $key }}">Награда RU</label>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-sm-12 col-md-6">
                                    <div class="form-group">
                                        <div class="form-material floating">
                                            <input type="text" name="levels[{{ $key }}][uz_reward]" value="{{ $level->uz_reward }}" id="uz_reward{{ $key }}" class="form-control">
                                            <label for="uz_reward{{ $key }}">Награда UZ</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    @endforeach
                </div>
            </div>
        </div>
    </form>
    <div class="block">
        <div class="block-header block-header-default">
            <h3 class="block-title">Топ рефоводов</h3>
        </div>
        <div class="block-content">
            <ul class="list-group list-group-flush">
                @foreach($topReferrals as $name => $count)
                    <li class="list-group-item">{{ $loop->index + 1 }}. {{ $name }} - {{ $count }}</li>
                @endforeach
            </ul>
        </div>
    </div>
    <template id="level-template">
        <div class="referral-level mt-20" style="border-bottom: 1px solid #eaecee;" id="referralLevel{0}">
            <div class="d-flex align-items-center justify-content-between">
                <h3 class="font-w600">Уровень</h3>
                <button class="btn btn-small btn-alt-danger btn-sm btn-rounded delete-button" type="button"
                        data-id="referralLevel{0}" data-toggle="tooltip" title="Удалить"><i class="si si-trash"></i>
                </button>
            </div>
            <label for="users_from{0}">Количество пользователей, которое необходимо набрать</label>
            <div class="row">
                <div class="col-sm-12 col-md-6">
                    <div class="form-group">
                        <div class="form-material">
                            <input type="number" name="levels[{0}][users_from]" id="users_from{0}" placeholder="От"
                                   class="form-control">
                        </div>
                    </div>
                </div>
                <div class="col-sm-12 col-md-6">
                    <div class="form-group">
                        <div class="form-material">
                            <input type="number" name="levels[{0}][users_to]" id="users_to{0}" placeholder="До"
                                   class="form-control">
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="row">
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group">
                            <div class="form-material floating">
                                <input type="text" name="levels[{0}][ru_reward]" id="ru_reward{0}" class="form-control">
                                <label for="ru_reward{0}">Награда RU</label>
                            </div>
                        </div>
                    </div>
                    <div class="col-sm-12 col-md-6">
                        <div class="form-group">
                            <div class="form-material floating">
                                <input type="text" name="levels[{0}][uz_reward]" id="uz_reward{0}" class="form-control">
                                <label for="uz_reward{0}">Награда UZ</label>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </template>
@endsection

@section('js')
    <script src="{{ asset('assets/js/plugins/bootstrap-datepicker/js/bootstrap-datepicker.min.js') }}"></script>
    <script>
        if (!String.prototype.format) {
            String.prototype.format = function () {
                var args = arguments;
                return this.replace(/{(\d+)}/g, function (match, number) {
                    return typeof args[number] != 'undefined'
                        ? args[number]
                        : match
                        ;
                });
            };
        }
        jQuery(function () {
            Codebase.helper('datepicker');
            let counter = {{ count($referral->levels) }};
            let templateString = $('#level-template').html();
            $('#addLevelButton').click(function (event) {
                counter++;
                let levelItemString = templateString.format(counter);
                let levelItem = $(levelItemString);
                levelItem.find('.delete-button').on('click', function (event) {
                    let deleteButton = $(this);
                    let levelItemId = deleteButton.data('id');
                    $(`#${levelItemId}`).remove();
                });
                $('#levels').append(levelItem);
            });
            $('.delete-button').on('click', function (event) {
                let deleteButton = $(this);
                let levelItemId = deleteButton.data('id');
                $(`#${levelItemId}`).remove();
            });
        });
    </script>
@endsection
