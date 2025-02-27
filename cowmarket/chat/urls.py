from django.urls import path
from .views import *

urlpatterns = [
    path("<int:user_id>/", chat_view, name="chat"),
    path("inbox/", chat_list, name="chat_list"),
]
