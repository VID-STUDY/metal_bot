<!doctype html>
<!--[if lte IE 9]>         <html lang="en" class="lt-ie10 lt-ie10-msg no-focus"> <![endif]-->
<!--[if gt IE 9]><!--> <html lang="en" class="no-focus"> <!--<![endif]-->
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=0">
    <meta name="csrf-token" content="{{ csrf_token() }}">

    <title>@yield('title') | TeleportBot</title>

    <meta name="description" content="Административная панель TeleportBot">
    <meta name="author" content="vid.uz">
    <meta name="robots" content="noindex, nofollow">

    <!-- Icons -->
    <!-- The following icons can be replaced with your own, they are used by desktop and mobile browsers -->
    <link rel="shortcut icon" href="{{ asset('assets/img/favicons/favicon.png') }}">
    <link rel="icon" type="image/png" sizes="192x192" href="{{ asset('assets/img/favicons/favicon-192x192.png') }}">
    <link rel="apple-touch-icon" sizes="180x180" href="{{ asset('assets/img/favicons/apple-touch-icon-180x180.png') }}">
    <!-- END Icons -->

    <!-- Stylesheets -->
    <!-- Codebase framework -->
    @yield('css')
    <link rel="stylesheet" id="css-main" href="{{ asset('assets/css/codebase.min.css') }}">

    <!-- You can include a specific file from css/themes/ folder to alter the default color theme of the template. eg: -->
    <!-- <link rel="stylesheet" id="css-theme" href="assets/css/themes/flat.min.css"> -->
    <!-- END Stylesheets -->
</head>
<body>
<div id="page-container" class="side-scroll page-header-modern main-content-boxed sidebar-o">
    {{--admin/layouts/partials/sidebar.blade.php--}}
    @include('layouts.partials.sidebar')

    {{--admin/layouts/partials/header.blade.php--}}
    @include('layouts.partials.header')

    <!-- Main Container -->
    <main id="main-container">
        <!-- Page Content -->
        <div class="content">
            {{-- Content --}}
            @yield('content')
        </div>
        <!-- END Page Content -->
    </main>
    <!-- END Main Container -->

    @include('layouts.partials.footer')
</div>
<!-- END Page Container -->

<!-- Codebase Core JS -->
<script src="{{ asset('assets/js/core/jquery.min.js') }}"></script>
<script src="{{ asset('assets/js/core/popper.min.js') }}"></script>
<script src="{{ asset('assets/js/core/bootstrap.min.js') }}"></script>
<script src="{{ asset('assets/js/codebase.min.js') }}"></script>
<script src="{{ asset('js/admin.js') }}"></script>
<script src="{{ asset('plugins/ckeditor/ckeditor.js') }}"></script>
<script src="{{ asset('plugins/ckfinder/ckfinder.js') }}"></script>
<script>
    $(function(){
        var editor = CKEDITOR.replaceAll(function (textarea, config) {
            config.enterMode = CKEDITOR.ENTER_BR;
        });
        CKFinder.setupCKEditor( editor );
    });

    var ru_datatable = {
        "sProcessing":   "Подождите...",
        "sLengthMenu":   "Показать _MENU_ записей",
        "sZeroRecords":  "Записи отсутствуют.",
        "sInfo":         "Записи с _START_ до _END_ из _TOTAL_ записей",
        "sInfoEmpty":    "Записи с 0 до 0 из 0 записей",
        "sInfoFiltered": "(отфильтровано из _MAX_ записей)",
        "sInfoPostFix":  "",
        "sSearch":       "Поиск:",
        "sUrl":          "",
        "oPaginate": {
            "sFirst": "Первая",
            "sPrevious": "Предыдущая",
            "sNext": "Следующая",
            "sLast": "Последняя"
        },
        "oAria": {
            "sSortAscending":  ": активировать для сортировки столбца по возрастанию",
            "sSortDescending": ": активировать для сортировки столбцов по убыванию"
        }
    };
    jQuery(function () {
        var userDropdown = function () {
            let userDropDownButton = $('#page-header-user-dropdown');
            userDropDownButton.on('click', function (e) {
                e.preventDefault();
                userDropDownButton.next().toggleClass('show');
                userDropDownButton.parent().toggleClass('show');
            })
        };
        userDropdown();

        var notificationsDropdown = function () {
            let userNotificationDropdown = jQuery('#page-header-notifications');
            userNotificationDropdown.on('click', function (e) {
                e.preventDefault();
                userNotificationDropdown.next().toggleClass('show');
                userNotificationDropdown.parent().toggleClass('show');
            });

            let userNotifications = jQuery('div[data-notification-id]');
            userNotifications.on('click', function (e) {
                let notificationId = $(this).data('notification-id');
                let url = "/account/notifications/markAsRead?id=" + notificationId;
                $.get(url);
            });
        };
        notificationsDropdown();
    });
</script>
@yield('js')
</body>
</html>
