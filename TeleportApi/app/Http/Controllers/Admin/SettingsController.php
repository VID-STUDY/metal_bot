<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Settings;
use Illuminate\Http\Request;

class SettingsController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $settings = Settings::first();
        if (!$settings) {
            $settings = Settings::create(['employer_tariff_1' => 7000,
                'employer_tariff_2' => 13000, 'employer_tariff_3' => 18000, 'contractor_tariff_1' => 1200,
                'contractor_tariff_2' => 1100, 'contractor_tariff_3' => 1000]);
        }
        return view('admin.settings.index', compact('settings'));
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $settings = Settings::first();
        if (!$settings) {
            $settings = Settings::create(['employer_tariff_1' => 7000,
                'employer_tariff_2' => 13000, 'employer_tariff_3' => 18000, 'contractor_tariff_1' => 1200,
                'contractor_tariff_2' => 1100, 'contractor_tariff_3' => 1000]);
        }
        $settings->update($request->all());
        return redirect()->route('admin.settings.index');
    }
}
