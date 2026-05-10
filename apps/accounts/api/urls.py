from django.urls import path
from apps.accounts.api.views import (
    UserRegistrationAPIView, VerifyUserRegistationOTPWithUserCreationAPIView,
    UserLoginAPIView, GoogleAuthAPIView
)


urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),

    path('login/', UserLoginAPIView.as_view(), name='login'),

    path('verify-register-otp/', VerifyUserRegistationOTPWithUserCreationAPIView.as_view(), name='verify-email-otp'),

    path('google/', GoogleAuthAPIView.as_view(), name='google'),
]