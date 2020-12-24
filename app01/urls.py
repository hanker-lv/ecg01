from django.urls import path,re_path
from app01 import views

urlpatterns = [
    path(r'index/', views.index),
    # path(r'upload/', views.upload),
    re_path(r'upload/(?P<person_id>\d+)/', views.upload),  #  正则表达式
    path(r'person_add/', views.person_add),
    # path(r'person_index/', views.person_index),
    re_path(r'person_index/(?P<person_id>\d+)/', views.person_index),
    # path(r'person_edit/', views.person_edit),
    re_path(r'person_edit/(?P<person_id>\d+)/', views.person_edit),
    # path(r'ecg_model/', views.ecg_model),
    re_path(r'ecg_model/(?P<person_id>\d+)/(?P<ecg_id>\d?)/', views.ecg_model),
    path(r'ann/', views.annoation),
]
