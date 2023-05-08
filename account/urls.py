from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
     path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
     path("create-user-profile/",views.CreateUserProfile, name="create_user_profile"),
     path('update-user-profile/', views.UpdateUserProfile, name='update_user_profile'),
     path("get-user-profile/",views.GetUserProfile, name="get_user_profile"),
     path("get-user-lists/",views.GetUsers, name="get_users"),
     path('forgot-password/', views.forgot_password, name='forgot-password'),
     path('reset-password/<str:uidb64>/<str:token>/', views.reset_password, name='reset-password'),
     path('verify-email/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
     path('games/', views.game_list, name='game_list'),
]
