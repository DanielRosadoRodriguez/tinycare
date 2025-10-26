import json
from pathlib import Path
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

BASE_DIR = Path(__file__).resolve().parents[2]  # .../tinycare/
CONTENT_FILE = BASE_DIR / "pages" / "content" / "landing_es.json"

def _load_copy() -> dict:
    with open(CONTENT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def home(request: HttpRequest) -> HttpResponse:
    data = _load_copy()
    return render(request, "pages/home.html", {"c": data})
