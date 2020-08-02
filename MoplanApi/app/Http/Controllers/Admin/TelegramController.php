<?php

namespace App\Http\Controllers\Admin;

use App\User;
use App\Http\Controllers\Controller;
use GuzzleHttp\Exception\ClientException;
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
            'image' => 'nullable',
            'text' => 'required|string|max:10000'
        ]);
        $text = $request->get('text');
        $text = str_replace('&nbsp;', ' ', $text);
        $text = str_replace('&mdash;', '-', $text);
        $text = strip_tags($text, ['b', 'i', 'u', 's', 'a', 'code', 'pre', 'strong', 'em']);
        if ($request->has('image')) {
            $image = $request->file('image');
            $mimeType = $image->getMimeType();

            if (strpos($mimeType, 'video') !== false)
                $this->sendVideo($image, $text);
            else
                $this->sendPhoto($image, $text);
        }
        else
            $this->sendText($text);
        return redirect()->route('admin.telegram.index');
    }

    private function sendPhoto(\Illuminate\Http\UploadedFile $image, string $text)
    {
        $users = User::where('name', '!=', 'Admin')->get();
        $client = new \GuzzleHttp\Client(array('base_uri' => 'https://api.telegram.org/bot' . env('TELEGRAM_BOT_TOKEN'). '/'));
        $imageFileId = null;
        foreach ($users as $user) {
            if ($imageFileId)
                $imageFile = $imageFileId;
            else
                $imageFile = fopen($image->getPath() . '/' . $image->getFilename(), 'r');
            try {
                $response = $client->post('sendPhoto', [
                    'multipart' => [
                        ['name' => 'photo', 'contents' => $imageFile],
                        ['name' => 'chat_id', 'contents' => $user->id],
                        ['name' => 'caption', 'contents' => $text],
                        ['name' => 'parse_mode', 'contents' => 'HTML']
                    ]
                ]);
                if (!$imageFileId) {
                    $jsonResult = json_decode($response->getBody()->getContents());
                    $imageFileId = end($jsonResult->result->photo)->file_id;
                }
            } catch (ClientException $e) {
                continue;
            }
        }
    }

    private function sendText(string $text)
    {
        $users = User::where('name', '!=', 'Admin')->get();
        $client = new \GuzzleHttp\Client(array('base_uri' => 'https://api.telegram.org/bot' . env('TELEGRAM_BOT_TOKEN'). '/'));
        foreach ($users as $user)
            $client->post('sendMessage', [
                'json' => ['chat_id' => $user->id, 'text' => $text, 'parse_mode' => 'HTML']
            ]);
    }

    private function sendVideo(\Illuminate\Http\UploadedFile $video, string $text)
    {
        $users = User::where('name', '!=', 'Admin')->get();
        $client = new \GuzzleHttp\Client(array('base_uri' => 'https://api.telegram.org/bot' . env('TELEGRAM_BOT_TOKEN'). '/'));
        $videoFileId = null;
        foreach ($users as $user) {
            if ($videoFileId)
                $videoFile = $videoFileId;
            else
                $videoFile = fopen($video->getPath() . '/' . $video->getFilename(), 'r');
            try {
                $response = $client->post('sendVideo', [
                    'multipart' => [
                        ['name' => 'video', 'contents' => $videoFile],
                        ['name' => 'chat_id', 'contents' => $user->id],
                        ['name' => 'caption', 'contents' => $text],
                        ['name' => 'parse_mode', 'contents' => 'HTML']
                    ]
                ]);
                if (!$videoFileId) {
                    $jsonResult = json_decode($response->getBody()->getContents());
                    $videoFileId = $jsonResult->result->video->file_id;
                }
            } catch (ClientException $e) {
                continue;
            }
        }
    }
}
