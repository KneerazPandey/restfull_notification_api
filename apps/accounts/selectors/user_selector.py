from django.contrib.auth import get_user_model


User = get_user_model()


class UserSelector:
    
    @staticmethod
    def is_existing_email(email):
        return User.objects.filter(email=email).exists()
    
    @staticmethod
    def get_first_filtered_user_by_email(email):
        return User.objects.filter(email=email).first()