from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema # <--- ADD THIS
from django.contrib.auth import get_user_model # <--- ADD THIS

from .serializers import SignupSerializer, MeSerializer, VerifyEmailSerializer
from .utils import set_verification_otp, send_verification_email

User = get_user_model() # <--- DEFINE USER HERE

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        try:
            otp = set_verification_otp(user)
            send_verification_email(user, otp)
        except Exception as e:
            print(f"🔥 ERROR in OTP/email: {e}")

        return Response(
            {"detail": "Account created. Check your email for a verification code."},
            status=status.HTTP_201_CREATED
        )

class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=VerifyEmailSerializer)
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Email verified successfully. You can now log in."}, status=status.HTTP_200_OK)

class ResendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=None, 
        responses={200: {"detail": "string"}},
        description="Provide 'email' in the request body to resend OTP."
    )
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            user = User.objects.get(email=email, is_email_verified=False)
            otp = set_verification_otp(user)
            send_verification_email(user, otp)
            return Response({"detail": "A new verification code has been sent."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found or already verified."}, status=status.HTTP_404_NOT_FOUND)

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(MeSerializer(request.user).data)