from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils import timezone
from .utils import send_welcome_email

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "full_name", "email", "phone", "role", "password"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user
    
class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "full_name", "email", "phone", "role", "created_at"]

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)

    def validate(self, attrs):
        email = attrs["email"]
        code = attrs["code"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid email or code.")

        if user.is_email_verified:
            raise serializers.ValidationError("Email already verified.")

        if not user.email_verification_code or not user.email_verification_expires_at:
            raise serializers.ValidationError("Error with verification code. Please sign up again.")

        if timezone.now() > user.email_verification_expires_at:
            raise serializers.ValidationError("Verification code expired.")

        if user.email_verification_code != code:
            raise serializers.ValidationError("Invalid email or code.")

        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        user.is_email_verified = True
        user.is_active = True
        user.email_verification_code = None
        user.email_verification_expires_at = None
        user.save(update_fields=[
            "is_email_verified",
            "is_active",
            "email_verification_code",
            "email_verification_expires_at"
        ])

        send_welcome_email(user)
        return user