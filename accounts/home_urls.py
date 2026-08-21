from django.urls import path
from . import views

urlpatterns = [
    path('', views.directory, name='directory'),
    path('pokes/', views.pokes_view, name='pokes'),
    path('about/', views.about, name='about'),
]
