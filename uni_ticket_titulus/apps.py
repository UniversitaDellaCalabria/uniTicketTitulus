from django.apps import AppConfig, apps
from django.core.exceptions import ImproperlyConfigured

from .settings import TITULUS_APP


class UniTicketTituluConfig(AppConfig):
    """App forms, utils and template for Titulus"""
    name = 'uni_ticket_titulus'
    verbose_name = 'Titulus interface'


    def ready(self):
        # Signals
        import uni_ticket_titulus.signals

        if not TITULUS_APP:
            raise ImproperlyConfigured(
                "PROTOCOL_ENABLED=True but PROTOCOL_APP is not set"
            )
        if not apps.is_installed(TITULUS_APP):
            raise ImproperlyConfigured(
                f"PROTOCOL_APP '{TITULUS_APP}' is not in INSTALLED_APPS"
            )
