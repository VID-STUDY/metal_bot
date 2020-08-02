@extends('layouts.app')

@section('title', 'Реферальная система')

@section('content')
    <div class="block">
        <div class="block-header block-header-default">
            <h3 class="block-title">Реферальные конкурсы</h3>
            <div class="block-options">
                <a href="{{ route('admin.referral.create') }}" class="btn btn-alt-primary"><i class="fa fa-plus"></i> Создать</a>
            </div>
        </div>
        <div class="block-content">
            <ul class="list-group list-group-flush mb-20">
                @foreach($referralTenders as $tender)
                    <li class="list-group-item d-flex justify-content-between align-items-center">{{ $tender->date_from }} - {{ $tender->date_to }}
                        <span class="d-flex">
                            <a href="{{ route('admin.referral.edit', $tender->id) }}" data-toggle="tooltip" title="Редактировать"
                               class="btn btn-sm btn-alt-info mr-10"><i class="fa fa-edit"></i></a>
                            <form action="{{ route('admin.referral.destroy', $tender->id) }}" method="post">
                                @csrf
                                @method('delete')
                                <button data-toggle="tooltip" onclick="return confirm('Вы уверены?')" title="Удалить" class="btn btn-sm btn-alt-danger"><i class="fa fa-trash"></i></button>
                            </form>
                        </span>
                    </li>
                @endforeach
            </ul>
        </div>
    </div>
@endsection
