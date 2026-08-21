from django.urls import path
from . import views

urlpatterns = [
    path('send/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('respond/<int:request_id>/<str:action>/', views.respond_to_request, name='respond_to_request'),
    path('requests/', views.friend_requests, name='friend_requests'),
    path('my_friends/', views.my_friends, name='my_friends'),
    path('remove/<int:user_id>/', views.remove_friend, name='remove_friend'),
]
