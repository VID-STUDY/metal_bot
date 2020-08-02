<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateSettingsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('settings', function (Blueprint $table) {
            $table->id();

            $table->integer('employer_tariff_1');
            $table->integer('employer_tariff_2');
            $table->integer('employer_tariff_3');
            $table->integer('contractor_tariff_1');
            $table->integer('contractor_tariff_2');
            $table->integer('contractor_tariff_3');

            $table->text('faq')->nullable();
            $table->text('about')->nullable();
            $table->text('partners')->nullable();
            $table->text('news')->nullable();

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
        Schema::dropIfExists('settings');
    }
}
