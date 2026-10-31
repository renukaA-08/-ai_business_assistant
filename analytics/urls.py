from django.urls import path
from analytics.views import chat_api , chat_page

urlpatterns = [
    path("", chat_page, name="chat_page"),
    path("chat/", chat_api, name="chat_api"),
]