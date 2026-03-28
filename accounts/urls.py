from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import SignupView, MeView, VerifyEmailView, ResendOTPView
from .tokens import VerifiedTokenObtainPairSerializer

class VerifiedTokenObtainPairView(TokenObtainPairView):
    serializer_class = VerifiedTokenObtainPairSerializer

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("auth/login/", VerifiedTokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("me/", MeView.as_view(), name="me"),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
]