from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('feed/', views.feed_view, name='feed'),
]
