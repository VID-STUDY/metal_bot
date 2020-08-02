<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class HandbookCategoriesDescription extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('handbook_categories', function (Blueprint $table) {
            $table->string('ru_description')->nullable();
            $table->string('uz_description')->nullable();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('handbook_categories', function (Blueprint $table) {
            $table->dropColumn('ru_description');
            $table->dropColumn('uz_description');
        });
    }
}
