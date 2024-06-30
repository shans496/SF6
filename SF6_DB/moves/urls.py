from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_move_names/', views.get_move_names, name='get_move_names'),
    path('get_strengths_and_derivatives/', views.get_strengths_and_derivatives, name='get_strengths_and_derivatives'),
]
