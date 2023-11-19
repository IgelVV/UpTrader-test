from django.shortcuts import render
from django.http import HttpRequest


def display_menu(request: HttpRequest):
    selected_item = request.GET.get("item")
    return render(
        request,
        "menu/index.html",
        context={"selected_item": selected_item},
    )
