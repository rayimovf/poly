from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, Token
from .models import CustomUser


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if not phone_number:
            raise serializers.ValidationError('Phone number is required')
        if not password:
            raise serializers.ValidationError('Password is required')
        return attrs



class UserSerializerWithName(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'phone_number')


class UserSerializerWithToken(serializers.ModelSerializer):
    access = serializers.SerializerMethodField(read_only=True)
    refresh = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'id', 'name', 'phone_number',
            'is_superuser', 'access', 'refresh',
            'isAdmin'
        )

    def get_access(self, user: CustomUser):
        token: Token = RefreshToken.for_user(user)
        return str(token.access_token)

    def get_refresh(self, user: CustomUser):
        token: Token = RefreshToken.for_user(user)
        return str(token)

    def get_isAdmin(self, user: CustomUser):
        return user.is_staff
