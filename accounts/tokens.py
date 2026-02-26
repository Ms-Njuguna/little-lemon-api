from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class VerifiedTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_email_verified:
            raise serializers.ValidationError("Please verify your email before logging in.")

        if not self.user.is_active:
            raise serializers.ValidationError("Account is inactive.")

        return data