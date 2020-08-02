<?php

namespace App;

use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    /**
     * The attributes that are mass assignable.
     *
     * @var array
     */
    protected $fillable = [
        'name', 'email', 'password', 'language', 'username', 'id', 'user_role',
        'referral_from_id', 'referral_tender_id', 'free_actions_count', 'balance_contractor', 'balance_employer',
        'employer_tariff', 'contractor_tariff'
    ];

    /**
     * The attributes that should be hidden for arrays.
     *
     * @var array
     */
    protected $hidden = [
        'password', 'remember_token',
    ];

    /**
     * The attributes that should be cast to native types.
     *
     * @var array
     */
    protected $casts = [
        'email_verified_at' => 'datetime',
    ];

    /**
     * User's resumes
     *
     * @return \Illuminate\Database\Eloquent\Relations\HasMany
     */
    public function resumes()
    {
        return $this->hasMany(Resume::class);
    }

    /**
     * User's vacations
     *
     * @return \Illuminate\Database\Eloquent\Relations\HasMany
     */
    public function vacations()
    {
        return $this->hasMany(Vacation::class);
    }

    public function referrals()
    {
        return $this->hasMany(User::class, 'referral_from_id', 'id');
    }

    public function referralFrom()
    {
        return $this->hasOne(User::class, 'id', 'referral_from_id');
    }

    public function paymentHistory()
    {
        return $this->hasMany(PaymentHistory::class, 'user_id', 'id');
    }
}
