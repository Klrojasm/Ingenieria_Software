<?php

namespace App\Http\Controllers;
use App\Models\Genre;
use Illuminate\Http\Request;
use App\Models\Band;

class GenreController extends Controller
{
    public function index()
    {
        return Genre::all();
    }
    public function show(string $id)
    {
        return Genre::with('bands')->get()->find($id);
    }
}
