from django.urls import path
from . import views
from .views import chat

urlpatterns = [
    path('', views.hello, name="hello"),
    path('chat/', chat, name='chat'),
]