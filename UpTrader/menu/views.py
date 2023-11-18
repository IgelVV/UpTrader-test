from django.shortcuts import render
from django.http import HttpRequest


def display_menu(request: HttpRequest):
    return render(request, "menu/index.html", {"menu": "placeholder"})
