<?php

namespace App\Http\Controllers;
use App\Models\Band;
use App\Models\Genre;
use Illuminate\Http\Request;

class BandController extends Controller
{
    public function index()
    {
        $bands = Band::all();
        return $bands;
    }

    public function show($id)
    {
        $band = Band::find($id); 
        if ($band === null) {
            return response()->json(['message' => 'Band not found'], 404);
        }
        return $band;
    }

}
