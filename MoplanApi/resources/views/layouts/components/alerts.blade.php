@if ($message = session()->get('success'))
    <div class="alert alert-success alert-dismissible fade show" role="alert">
        <button class="close" type="button" data-dismiss="alert" aria-label="close">
            <span aria-hidden="true">&times;</span>
        </button>
        <h4 class="alert-heading">Готово!</h4>
        <p>{{ $message }}</p>
    </div>
@endif

@if ($message = session()->get('error'))
    <div class="alert alert-danger alert-dismissible fade show" role="alert">
        <button class="close" type="button" data-dismiss="alert" aria-label="close">
            <span aria-hidden="true">&times;</span>
        </button>
        <h4 class="alert-heading">Ошибка!</h4>
        <p>{{ $message }}</p>
    </div>
@endif
@if ($message = session()->get('warning'))
    <div class="alert alert-warning alert-dismissible fade show" role="alert">
        <button class="close" type="button" data-dismiss="alert" aria-label="close">
            <span aria-hidden="true">&times;</span>
        </button>
        <h4 class="alert-heading">Внимание!</h4>
        <p>{{ $message }}</p>
    </div>
@endif
@if ($message = session()->get('info'))
    <div class="alert alert-info alert-dismissible fade show" role="alert">
        <button class="close" type="button" data-dismiss="alert" aria-label="close">
            <span aria-hidden="true">&times;</span>
        </button>
        <h4 class="alert-heading">Информация!</h4>
        <p>{{ $message }}</p>
    </div>
@endif
