@extends('layouts.app')

@section('title', 'Административная панель')

@section('content')
    <h2 class="content-heading">Статистика</h2>
    <div class="row">
        <div class="col-md-6 col-xl-4">
            <div class="block block-transparent">
                <div class="block-content block-content-full bg-info">
                    <div class="py-20 text-center">
                        <div class="mb-20">
                            <i class="si si-users fa-4x text-info-light"></i>
                        </div>
                        <div class="font-size-h3 font-w600 text-white">{{ $usersCount }}</div>
                        <div class="font-size-sm font-w600 text-uppercase text-info-light">Всего пользователей</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-xl-4">
            <div class="block block-transparent">
                <div class="block-content block-content-full bg-success">
                    <div class="py-20 text-center">
                        <div class="mb-20">
                            <i class="si si-briefcase fa-4x text-info-light"></i>
                        </div>
                        <div class="font-size-h3 font-w600 text-white">{{ $vacationsCount }}</div>
                        <div class="font-size-sm font-w600 text-uppercase text-info-light">Всего объявлений на продажу</div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-md-6 col-xl-4">
            <div class="block block-transparent">
                <div class="block-content block-content-full bg-gd-leaf">
                    <div class="py-20 text-center">
                        <div class="mb-20">
                            <i class="si si-docs fa-4x text-info-light"></i>
                        </div>
                        <div class="font-size-h3 font-w600 text-white">{{ $resumesCount }}</div>
                        <div class="font-size-sm font-w600 text-uppercase text-info-light">Всего объявлений на закупку</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="block">
        <div class="block-header">
            <h3 class="block-title">Пользователей за последние 7 дней</h3>
        </div>
        <div class="block-content">
            <div class="">
                <div class="chartjs-size-monitor"></div>
                <canvas id="js-chartjs-dashboard-lines" class="js-chartjs-dashboard-lines chartjs-render-monitor" width="551" height="150"></canvas>
            </div>
        </div>
    </div>
    <h2 class="content-heading">Статистика</h2>
    <div class="block">
        <div class="block-header">
            <h3 class="block-title">Статистика категорий</h3>
        </div>
        <div class="block-content">
            <div class="table-responsive">
                <table class="table table-stripped table-bordered table-vcenter">
                    <thead>
                        <tr>
                            <th class="text-center">Должность</th>
                            <th class="text-center">Количество объявлений</th>
                            <th class="text-center">Количество закупок</th>
                        </tr>
                    </thead>
                    <tbody>
                        @foreach($statistics as $key => $item)
                            <tr>
                                <td class="text-center">{{ $key }}</td>
                                <td class="text-center">{{ $item['vacations'] }}</td>
                                <td class="text-center">{{ $item['resumes'] }}</td>
                            </tr>
                        @endforeach
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <template id="chartData">
        <ul id="dates">
            @foreach($weekUsersCount as $date => $count)
                <li>{{ $date }}</li>
            @endforeach
        </ul>
        <ul id="counts">
            @foreach($weekUsersCount as $date => $count)
                <li>{{ $count }}</li>
            @endforeach
        </ul>
    </template>
@endsection

@section('js')
    <script src="{{ asset('assets/js/plugins/chartjs/Chart.min.js') }}"></script>
    <script>
        var initDashboardChartJs = function () {
            Chart.defaults.global.defaultFontColor              = '#555555';
            Chart.defaults.scale.gridLines.color                = "transparent";
            Chart.defaults.scale.gridLines.zeroLineColor        = "transparent";
            Chart.defaults.scale.ticks.beginAtZero              = true;
            Chart.defaults.global.elements.line.borderWidth     = 2;
            Chart.defaults.global.elements.point.radius         = 5;
            Chart.defaults.global.elements.point.hoverRadius    = 7;
            Chart.defaults.global.tooltips.cornerRadius         = 3;
            Chart.defaults.global.legend.display                = false;
            var chartDashboardLinesCon  = document.getElementById('js-chartjs-dashboard-lines');

            // Lines Charts Data
            var chartDashboardLinesData = {
                labels : [
                    @foreach($weekUsersCount as $date => $count)
                        '{{ $date }}',
                    @endforeach
                ],
                datasets: [
                    {
                        label: 'This Week',
                        fill: true,
                        backgroundColor: 'rgba(66,165,245,.25)',
                        borderColor: 'rgba(66,165,245,1)',
                        pointBackgroundColor: 'rgba(66,165,245,1)',
                        pointBorderColor: '#fff',
                        pointHoverBackgroundColor: '#fff',
                        pointHoverBorderColor: 'rgba(66,165,245,1)',
                        data: [
                            @foreach($weekUsersCount as $date => $count)
                            {{ $count }},
                            @endforeach
                        ]
                    }
                ]
            };

            var chartDashboardLinesOptions = {
                scales: {
                    yAxes: [{
                        ticks: {
                            suggestedMax: 50
                        }
                    }]
                },
                tooltips: {
                    callbacks: {
                        label: function(tooltipItems, data) {
                            return ' ' + tooltipItems.yLabel + ' пользователей';
                        }
                    }
                }
            };

            new Chart(chartDashboardLinesCon,
                {
                    type: 'line',
                    data: chartDashboardLinesData,
                    options: chartDashboardLinesOptions
                });
        };
        jQuery(initDashboardChartJs);
    </script>
@endsection
