from django.urls import path,re_path
from login import views

urlpatterns = [
    path(r'login/', views.login),
    path(r'register/', views.register),
    path(r'logout/', views.logout),
]