<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class UzbekLangSettings extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('settings', function (Blueprint $table) {
            $table->text('faq_uz')->nullable();
            $table->text('about_uz')->nullable();
            $table->text('partners_uz')->nullable();
            $table->text('news_uz')->nullable();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('settings', function (Blueprint $table) {
            $table->dropColumn('faq_uz');
            $table->dropColumn('about_uz');
            $table->dropColumn('partners_uz');
            $table->dropColumn('news_uz');
        });
    }
}
