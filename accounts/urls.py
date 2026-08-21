from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('classmates/<str:course>/', views.classmates, name='classmates'),
    path('poke/<int:user_id>/', views.send_poke, name='send_poke'),
    path('poke/remove/<int:poke_id>/', views.remove_poke, name='remove_poke'),
]
