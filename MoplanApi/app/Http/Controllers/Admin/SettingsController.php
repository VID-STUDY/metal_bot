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
        $settings = Settings::get();
        $data = $request->all();
        foreach ($data as $key => $value) {
            $data[$key] = str_replace('&nbsp;', ' ', $data[$key]);
            $data[$key] = str_replace('&mdash;', '-', $data[$key]);
            $data[$key] = strip_tags($data[$key], ['b', 'i', 'u', 's', 'a', 'code', 'pre', 'strong', 'em', 'br']);
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
