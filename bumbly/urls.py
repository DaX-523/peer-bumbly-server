from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello, name='hello'),
    # path('users/', views.UserListCreate.as_view(), name='users'),
    # path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('users/', views.users, name='users'),
]