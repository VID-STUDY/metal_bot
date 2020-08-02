<?php

namespace App\Http\Controllers\Admin;

use App\HandbookCategory;
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
        $dayEnd = now()->endOfDay();
        $dayStart = now()->startOfDay();
//        $usersToday = User::where('created_at', '<', $dayEnd)->where('created_at', '>', $dayStart)->count();
//        $vacationsToday = Vacation::where('created_at', '<', $dayEnd)->where('created_at', '>', $dayStart)->count();
//        $resumesToday = Resume::where('created_at', '<', $dayEnd)->where('created_at', '>', $dayStart)->count();
        $usersCount = User::count();
        $vacationsCount = Vacation::count();
        $resumesCount = Resume::count();
        $oneWeekAgo = now()->subDays(6)->startOfDay();
        $weekUsersCount = User::where('created_at', '>=', $oneWeekAgo)
            ->groupBy('date')
            ->orderBy('date', 'ASC')
            ->get(array(
                DB::raw('Date(created_at) as "date"'),
                DB::raw('COUNT(*) as "count"')
            ))->pluck('count', 'date');

        $positions = collect();
        $allCategories = HandbookCategory::all();
        foreach ($allCategories as $category) {
            if (!$category->hasCategories())
                $positions->add($category);
        }
        $statistics = collect();
        foreach ($positions as $position) {
            $statistics->put($position->ru_title, [
                'vacations' => $position->vacations()->count(),
                'resumes' => $position->resumes()->count()
            ]);
        }

        return view('admin.index', compact('usersCount', 'vacationsCount', 'resumesCount', 'weekUsersCount', 'statistics'));
    }
}
