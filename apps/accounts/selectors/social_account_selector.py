from apps.accounts.models import SocialAccount


class SocialAccountSelector:

    @staticmethod
    def get_social_account_by_provider(provider):
        return SocialAccount.objects.filter(provider=provider)
    
    @staticmethod
    def get_social_account_by_provider_uid(provider_uid):
        return SocialAccount.objects.filter(provider_uid=provider_uid)
    
    @staticmethod
    def get_soical_account_by_provider_and_provider_uid(provider, provider_uid):
        return SocialAccount.objects.filter(
            provicer=provider,
            provider_uid=provider_uid,
        )