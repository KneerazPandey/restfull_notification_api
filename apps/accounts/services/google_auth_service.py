from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.selectors import SocialAccountSelector, UserSelector
from apps.accounts.models import SocialAccount


User = get_user_model()


class GoogleAuthService:

    @staticmethod
    def verify_google_token(token: str):
        try:
            data = id_token.verify_oauth2_token(
                token,
                request=requests.Request(),
                audience=settings.GOOGLE_CLIENT_ID
            )

            return data 
        except Exception:
            return None
        
    @staticmethod
    def login_or_register(google_data):
        email = google_data.get("email")
        google_id = google_data.get("sub")  # unique google user id
        
        if not email:
            raise ValueError("Google account has no email")

        email = email.lower().strip()

        social_account = SocialAccountSelector.get_soical_account_by_provider_and_provider_uid(
            provider='google',
            provider_uid=google_id
        ).first()

        if social_account:
            user = social_account.user
        else:
            user = UserSelector.get_first_filtered_user_by_email(email=email)
            if not user:
                user = User.objects.create(
                    email=email,
                    is_verified=True
                )
            
            SocialAccount.objects.create(
                user=user,
                provider="google",
                provider_uid=google_id,
                extra_data=google_data
            )

        
        refresh = RefreshToken.for_user(user)
        
        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }