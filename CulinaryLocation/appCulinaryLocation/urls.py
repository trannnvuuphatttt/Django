import ckeditor_uploader
from django.urls import path, re_path, include
from . import views
from .admin import admin_site
from .views import chat

urlpatterns = [
    path('', views.hello, name="hello"),
    path('chat/', chat, name='chat'),
    path('admin/', admin_site.urls),
]