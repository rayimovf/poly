from django.core import exceptions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework.permissions import IsAuthenticated

from utils.render_response import render_message, render_data
from ...models import CustomUser
from ...serializers import LoginSerializer, UserSerializerWithToken


class RegisterGenericAPIView(GenericAPIView):
    queryset = CustomUser
    serializer_class = UserSerializerWithToken


class AuthUserView(RegisterGenericAPIView):

    def post(self, request):
        try:
            custom_user = self.queryset.objects.create_user(
                phone_number=request.data['phone_number'],
                password=request.data['password'],
            )
            user_serializer = self.serializer_class(custom_user, many=False)
            return Response(
                render_data(data=user_serializer.data, success='true'),
                status = status.HTTP_201_CREATED
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class LoginView(APIView):
    queryset = CustomUser

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            try:
                user = self.queryset.objects.get(phone_number=phone_number)
            except exceptions.ObjectDoesNotExist:
                return Response(
                    render_message(message='User not found', success='false'),
                    status = status.HTTP_404_NOT_FOUND
                )

            if not user.check_password(password):
                return Response(
                    render_message(message='Incorrect password', success='false'),
                    status = status.HTTP_400_BAD_REQUEST
                )
            if not user.is_active:
                return Response(
                    render_message(message='Inactive account', success='false'),
                    status = status.HTTP_400_BAD_REQUEST
                )
            serializer = UserSerializerWithToken(user)
            return Response(
                render_data(data=serializer.data, success='true'),
                status = status.HTTP_200_OK
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                render_message(message='Logged out successfully', success='true'),
                status = status.HTTP_205_RESET_CONTENT
            )
        except Exception as error:
            return Response(
                render_message(message=str(error), success='false'),
                status = status.HTTP_400_BAD_REQUEST
            )