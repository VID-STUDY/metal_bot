<?php

namespace App\Http\Controllers\Admin;

use App\User;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class TelegramController extends Controller
{
    public function index()
    {
        return view('admin.telegram.index');
    }

    public function distribution(Request $request)
    {
        $request->validate([
            'image' => 'nullable|image|mimes:jpeg,png,jpg,gif',
            'text' => 'required|string|max:10000'
        ]);
        $users = User::where('name', '!=', 'Admin')->get();
        $client = new \GuzzleHttp\Client(array('base_uri' => 'https://api.telegram.org/bot' . env('TELEGRAM_BOT_TOKEN'). '/'));
        $text = $request->get('text');
        $text = str_replace('<br />', "", $text);
        $text = str_replace('&nbsp;', ' ', $text);
        if ($request->has('image'))
        {
            $image = $request->file('image');
            $image = fopen($image->getPath() . '/' . $image->getFilename(), 'r');
            foreach ($users as $user)
                $client->post('sendPhoto', [
                    'multipart' => [
                        [ 'name' => 'photo', 'contents' => $image ],
                        [ 'name' => 'chat_id', 'contents' => $user->id ],
                        [ 'name' => 'caption', 'contents' => $text ],
                        [ 'name' => 'parse_mode', 'contents' => 'HTML' ]
                    ]
                ]);
        }
        else
            foreach ($users as $user)
                $client->post('sendMessage', [
                    'json' => ['chat_id' => $user->id, 'text' => $text, 'parse_mode' => 'HTML']
                ]);
        return redirect()->route('admin.telegram.index');
    }
}
