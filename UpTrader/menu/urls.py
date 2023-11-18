from django.urls import path

from .views import display_menu


app_name = "menu"

urlpatterns = [
    path('', display_menu, name="index")
]
