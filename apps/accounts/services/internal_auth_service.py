from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from core.utils import Otp
from apps.accounts.selectors import UserSelector


User = get_user_model()


class InternalAuthService:

    @staticmethod
    def initiate_user_registration(email: str, password: str):
        email = email.strip().lower()

        if UserSelector.is_existing_email(email=email):
            raise ValueError("User with this email already exists")
        
        cache_key = f'auth:register:{email}'
        otp = Otp.generate_random_otp()
        data = {
            'email': email,
            'otp': otp,
            'password': make_password(password=password)
        }
        cache.set(
            cache_key,
            data,
            timeout=300
        )

        return otp
    

    @staticmethod
    def verify_registration_otp_with_user_creation(email: str, otp: str):
        email = email.lower().strip()
        cache_key = f'auth:register:{email}'
        data = cache.get(cache_key)

        if not data:
            raise ValueError("OTP expired or invalid request")
        
        attempts = data.get('attempts', 0)
        if attempts > 3:
            cache.delete(cache_key)
            raise ValueError('All 3 attempt failed. Please enter registration details again to get new otp.')

        if data["otp"] != otp:
            data["attempts"] = data.get("attempts", 1) + 1
            cache.set(cache_key, data, timeout=300)
            raise ValueError('Invalid Otp. Please try again.')
        

        user = User.objects.create(
            email=email,
            password=data["password"],
            is_verified=True
        )

        cache.delete(cache_key)

        return user 
    

    @staticmethod
    def login_user(email: str, password: str):
        email = email.lower().strip()
        user = authenticate(email=email, password=password)

        if not user:
            raise ValueError("Invalid credentials")

        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }



        


