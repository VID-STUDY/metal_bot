<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Settings;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\File;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class SettingsController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        $settings = Settings::get();
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
        $data = $request->all();
        $data['about'] = str_replace('&nbsp;', ' ', $data['about']);
        $data['about'] = str_replace('&mdash;', '-', $data['about']);
        $data['about_uz'] = str_replace('&nbsp;', ' ', $data['about_uz']);
        $data['about_uz'] = str_replace('&mdash;', '-', $data['about_uz']);
        $data['news'] = str_replace('&nbsp;', ' ', $data['news']);
        $data['news'] = str_replace('&mdash;', '-', $data['news']);
        $data['news_uz'] = str_replace('&nbsp;', ' ', $data['news_uz']);
        $data['news_uz'] = str_replace('&mdash;', '-', $data['news_uz']);
        $data['partners'] = str_replace('&nbsp;', ' ', $data['partners']);
        $data['partners'] = str_replace('&mdash;', '-', $data['partners']);
        $data['partners_uz'] = str_replace('&nbsp;', ' ', $data['partners_uz']);
        $data['partners_uz'] = str_replace('&mdash;', '-', $data['partners_uz']);
        $data['partners_tariffs'] = str_replace('&nbsp;', ' ', $data['partners_tariffs']);
        $data['partners_tariffs'] = str_replace('&mdash;', '-', $data['partners_tariffs']);
        $data['partners_tariffs_uz'] = str_replace('&nbsp;', ' ', $data['partners_tariffs_uz']);
        $data['partners_tariffs_uz'] = str_replace('&mdash;', '-', $data['partners_tariffs_uz']);
        $data['faq'] = str_replace('&nbsp;', ' ', $data['faq']);
        $data['faq'] = str_replace('&mdash;', '-', $data['faq']);
        $data['faq_uz'] = str_replace('&nbsp;', ' ', $data['faq_uz']);
        $data['faq_uz'] = str_replace('&mdash;', '-', $data['faq_uz']);
        if (!$settings) {
            $settings = Settings::create(['employer_tariff_1' => 7000,
                'employer_tariff_2' => 13000, 'employer_tariff_3' => 18000, 'contractor_tariff_1' => 1200,
                'contractor_tariff_2' => 1100, 'contractor_tariff_3' => 1000]);
        }
        $settings->update($data);
        $image = $request->file('partners_ad_image');
        if ($image) {
            $extension = $image->getClientOriginalExtension();
            $filename = Str::random() . '.' . $extension;
            $filepath = Storage::disk('public')->getDriver()->getAdapter()->getPathPrefix() . $filename;
            Storage::disk('public')->put($filename, File::get($image));
            $settings->partners_ad_image = $filepath;
            $settings->save();
        }
        $image = $request->file('partners_ad_image_uz');
        if ($image) {
            $extension = $image->getClientOriginalExtension();
            $filename = Str::random() . '.' . $extension;
            $filepath = Storage::disk('public')->getDriver()->getAdapter()->getPathPrefix() . $filename;
            Storage::disk('public')->put($filename, File::get($image));
            $settings->partners_ad_image_uz = $filepath;
            $settings->save();
        }
        return redirect()->route('admin.settings.index');
    }

    public function deleteAdImage(string $language)
    {
        $settings = Settings::get();
        $filepath = $settings->partners_ad_image;
        if ($language == 'uz')
            $filepath = $settings->partners_ad_image_uz;
        if (File::exists($filepath)) {
            File::delete($filepath);
        }
        if ($language == 'uz') {
            $settings->partners_ad_image_uz = null;
        } else {
            $settings->partners_ad_image = null;
        }
        $settings->save();
        return redirect()->route('admin.settings.index');
    }
}
