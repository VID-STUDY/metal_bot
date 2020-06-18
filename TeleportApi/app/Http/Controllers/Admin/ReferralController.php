<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\ReferralTender;
use Illuminate\Http\Request;

class ReferralController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $referralTenders = ReferralTender::all();
        return view('admin.referral.index', compact('referralTenders'));
    }

    /**
     * Show the form for creating a new resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function create()
    {
        return view('admin.referral.create');
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $request->validate([
            'date_from' => 'required|date',
            'date_to' => 'required|date',
            'ru_description' => 'required|string',
            'uz_description' => 'required|string',
            'total_pot' => 'required|integer'
        ]);
        $referralTender = ReferralTender::create($request->all());
        foreach ($request->get('levels') as $level) {
            $referralTender->levels()->create($level);
        }
        return redirect()->route('admin.referral.index');
    }

    /**
     * Show the form for editing the specified resource.
     *
     * @param ReferralTender $referral
     * @return \Illuminate\Http\Response
     */
    public function edit(ReferralTender $referral)
    {
        return view('admin.referral.edit', compact('referral'));
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\ReferralTender  $referral
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, ReferralTender $referral)
    {
        $request->validate([
            'date_from' => 'required|date',
            'date_to' => 'required|date',
            'ru_description' => 'required|string',
            'uz_description' => 'required|string',
            'total_pot' => 'required|integer'
        ]);
        $referral->update($request->all());
        $referral->levels()->delete();
        foreach ($request->get('levels') as $level) {
            $referral->levels()->create($level);
        }
        return redirect()->route('admin.referral.index');
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param \App\ReferralTender $referral
     * @return \Illuminate\Http\Response
     * @throws \Exception
     */
    public function destroy(ReferralTender $referral)
    {
        $referral->levels()->delete();
        $referral->delete();
        return redirect()->route('admin.referral.index');
    }
}
