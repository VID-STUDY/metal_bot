<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateReferralTenderLevelsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('referral_tender_levels', function (Blueprint $table) {
            $table->id();

            $table->integer('users_from');
            $table->integer('users_to');
            $table->string('ru_reward')->nullable();
            $table->string('uz_reward')->nullable();

            $table->integer('referral_tender_id')->unsigned();

            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('referral_tender_levels');
    }
}
