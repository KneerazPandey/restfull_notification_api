from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from apps.accounts.services import InternalAuthService, GoogleAuthService
from apps.accounts.api.serializers import (
    RegisterSerializer, VerifyOTPSerializer, LoginSerializer, UserSerializer,
    GoogleAuthSerializer
)



class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = InternalAuthService.initiate_user_registration(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        return Response({
            'email': serializer.validated_data['email'],
            'otp': otp,
            'message': 'Otp has been sent to your email address.'
        })


class VerifyUserRegistationOTPWithUserCreationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        InternalAuthService.verify_registration_otp_with_user_creation(
            email=serializer.validated_data['email'],
            otp=serializer.validated_data['otp']
        )

        return Response({
            'email': serializer.validated_data['email'],
            'message': 'Email verified successfully'
        }, status=status.HTTP_201_CREATED)
    


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request, **kwargs):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        data = InternalAuthService.login_user(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        user_data = UserSerializer(data['user']).data

        return Response({
            'message': 'Login successfull',
            'user': user_data,
            'access': data['access'],
            'refresh': data['refresh']
        })
    



class GoogleAuthAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = GoogleAuthSerializer(data=request.data)
        token = serializer.validated_data["id_token"]

        google_data = GoogleAuthService.verify_google_token(token)

        if not google_data:
            return Response(
                {"error": "Invalid Google token"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        result = GoogleAuthService.login_or_register(
            google_data=google_data,
        )

        return Response({
            "user": UserSerializer(result["user"]).data,
            "access": result["access"],
            "refresh": result["refresh"]
        })
