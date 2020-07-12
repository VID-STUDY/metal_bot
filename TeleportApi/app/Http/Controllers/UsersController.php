<?php

namespace App\Http\Controllers;

use App\User;
use App\ReferralTender;
use Illuminate\Http\Request;

class UsersController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        return User::all();
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        $user = User::create($request->all());
        if ($user->referral_from_id) {
            $now = now()->format('Y-m-d');
            $tender = ReferralTender::where('date_from', '<=', $now)->where('date_to', '>=', $now)->first();
            if ($tender) {
                $user->referral_tender_id = $tender->id;
                $user->save();
                $referralUser = $user->referralFrom;
                $referralsCount = $referralUser->referrals()->where('referral_tender_id', $tender->id)->count();
                foreach($tender->levels as $level)
                {
                    if ($referralsCount == $level->users_to) {
                        $bonus = intval($level->ru_reward);
                        $referralUser->free_actions_count += $bonus;
                        $referralUser->save();
                    }
                }
            }
        }
        return response()->json($user, 201);
    }

    /**
     * Show user
     *
     * @param User $user
     * @return User
     */
    public function show(User $user)
    {
        return $user;
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\User  $user
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, User $user)
    {
        $user->update($request->all());

        if ($request->has('add_to_payment_history')) {
            $user->paymentHistory()->create(['amount' => $request->get('add_to_payment_history')]);
        }

        return response()->json($user, 200);
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param \App\User $user
     * @return \Illuminate\Http\Response
     * @throws \Exception
     */
    public function destroy(User $user)
    {
        $user->delete();

        return response()->json(null, 204);
    }

    /**
     * Get user resumes
     *
     * @param User $user
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function getResumes(User $user) {
        return $user->resumes()->get();
    }


    /**
     * Get user vacations
     *
     * @param User $user
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function getVacations(User $user) {
        return $user->vacations()->get();
    }

    public function getPaymentHistory(Request $request, User $user)
    {
        $query = $user->paymentHistory();
        if ($request->has('limit'))
            $query = $query->limit(intval($request->get('limit')));
        return $query->get();
    }
}
