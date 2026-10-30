from django.conf import settings


DEFAULT_TITULUS_APP = getattr(settings, "DEFAULT_TITULUS_APP", "titulus_utility")

# in settingslocal.py
# TITULUS_NOTIFICATION_AUTH='your_auth_token'