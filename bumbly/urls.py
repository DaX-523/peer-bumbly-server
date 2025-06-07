from django.urls import path
from .views import views, auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', auth_views.Home.as_view(), name='hello'),
    #  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #these are default django auth views these work well with sql
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),   # but not nosql so we use our own custom views
    # path('users/', views.UserListCreate.as_view(), name='users'),
    # path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    path('users/', views.users, name='users'),
    path('signup/', auth_views.signup, name='signup'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
]