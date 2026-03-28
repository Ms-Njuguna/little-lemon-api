from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import SignupSerializer, MeSerializer, VerifyEmailSerializer
from .utils import set_verification_otp, send_verification_email

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        try:
            otp = set_verification_otp(user)
            print(f"OTP generated: {otp}")

            send_verification_email(user, otp)
            print("Email sent successfully")

        except Exception as e:
            print(f"🔥 ERROR in OTP/email: {e}")

        return Response(
            {"detail": "Account created. Check your email for a verification code."},
            status=status.HTTP_201_CREATED
        )

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(MeSerializer(request.user).data)
    
class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Email verified successfully. You can now log in."}, status=status.HTTP_200_OK)