<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateReferralTendersTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('referral_tenders', function (Blueprint $table) {
            $table->id();

            $table->date('date_from');
            $table->date('date_to');
            $table->text('ru_description');
            $table->text('uz_description');
            $table->integer('total_pot');

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
        Schema::dropIfExists('referral_tenders');
    }
}
