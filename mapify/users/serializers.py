from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering a new user."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    """Serializer for logging in an existing user."""
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        if not user.check_password(data['password']):
            raise serializers.ValidationError("Incorrect credentials")
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
