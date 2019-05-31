from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index),
    re_path('^index$', views.index),
    path('addName/', views.add_name),
    path('remove/', views.remove),
    path('getSn/', views.create_sn),
]
