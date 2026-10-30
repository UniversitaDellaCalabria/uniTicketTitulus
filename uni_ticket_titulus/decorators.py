import hmac
import logging
from functools import wraps
from django.conf import settings
from django.http import HttpResponseServerError, HttpResponseForbidden


logger = logging.getLogger(__name__)


def require_titulus_auth(view_func):
    """
    Decoratore per validare l'header Authorization delle chiamate webhook di Titulus.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        expected_token = getattr(settings, 'TITULUS_NOTIFICATION_AUTH', None)

        # Sicurezza: se ci scordiamo di configurare il token, blocchiamo tutto per evitare falle
        if not expected_token:
            logger.error("[Webhook Auth] TITULUS_NOTIFICATION_AUTH non è configurato in settings.py!")
            return HttpResponseServerError("Server misconfigured.")

        # Recuperiamo l'header (Django popola request.headers in automatico)
        auth_header = request.headers.get('Authorization')

        # Verifichiamo la presenza del token e la sua correttezza
        if not auth_header or not hmac.compare_digest(auth_header, expected_token):
            client_ip = request.META.get('REMOTE_ADDR', 'IP_SCONOSCIUTO')
            logger.warning(
                f"[Webhook Auth] Tentativo di accesso negato da IP {client_ip}. Header Auth errato o mancante.")
            return HttpResponseForbidden("Non autorizzato")  # Restituisce errore 403

        # Se passa il controllo, eseguiamo la view
        return view_func(request, *args, **kwargs)

    return _wrapped_view