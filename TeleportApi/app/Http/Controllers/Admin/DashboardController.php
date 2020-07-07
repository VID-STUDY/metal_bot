<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\User;
use App\Resume;
use App\Vacation;
use Illuminate\Support\Facades\DB;

class DashboardController extends Controller
{
    public function index()
    {
        $dayEnd = now()->endOfDay()->format('Y-m-d');
        $dayStart = now()->startOfDay()->format('Y-m-d');
        $usersToday = User::where('created_at', '<', $dayEnd)->where('created_at', '>', $dayStart)->count();
        $vacationsToday = Vacation::where('created_at', '<', $dayEnd)->where('created_at', '>', $dayStart)->count();
        $resumesToday = Resume::where('created_at', '<', $dayEnd)->where('created_at', '>', $dayStart)->count();
        $oneWeekAgo = now()->subDays(6)->startOfDay()->format('Y-m-d');
        $weekUsersCount = User::where('created_at', '>=', $oneWeekAgo)
            ->groupBy('date')
            ->orderBy('date', 'ASC')
            ->get(array(
                DB::raw('Date(created_at) as "date"'),
                DB::raw('COUNT(*) as "count"')
            ))->pluck('count', 'date');

        return view('admin.index', compact('usersToday', 'vacationsToday', 'resumesToday', 'weekUsersCount'));
    }
}
