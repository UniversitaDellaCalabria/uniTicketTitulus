import logging
import json

from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.utils import timezone

from uni_ticket.models import Ticket

from ..decorators import require_titulus_auth
from ..utils import *


logger = logging.getLogger(__name__)


# @csrf_exempt
@require_titulus_auth
def endpoint_titulus_webhook(request):
    logger.debug(f"[u:Titulus-Webhook] {request}")
    if request.method == 'GET':
        nrecord_ricevuto = request.GET.get('titRecord')
        request_data = {
            "method": request.method,
            "path": request.path,
            "full_url": request.build_absolute_uri(),
            "headers": dict(request.headers),  # Tutti gli header (User-Agent, Content-Type, ecc.)
            "query_params": dict(request.GET),  # Parametri passati nell'URL (?param=value)
            "client_ip": request.META.get('REMOTE_ADDR'),  # IP di chi fa la chiamata
        }
        formatted_info = json.dumps(request_data, indent=4)
        logger.debug(f"Dettagli completi della richiesta:\n{formatted_info}")
        logger.info(f"[u:Titulus-Webhook] Ricevuta notifica protocollazione, nrecord: {nrecord_ricevuto}")

        if nrecord_ricevuto:
            tickets = Ticket.objects.filter(
                Q(protocol_number__isnull=True) | Q(protocol_number=""),
                protocol_nrecord=nrecord_ricevuto, 
                draft=False
            ).select_related(
                'input_module__ticket_category__organizational_structure'
            )

            if not tickets.exists():
                logger.error(f"[u:Titulus-Webhook] Ricevuto un NRECORD non registrato, nrecord: {nrecord_ricevuto}")
                return HttpResponse("OK", status=200)
            if tickets.count() > 1:
                logger.error(
                    f"[u:Titulus-Webhook] Ricevuto un NRECORD associato a più notifiche, nrecord: {nrecord_ricevuto}")
                return HttpResponse("OK", status=200)
            ticket = tickets.first()
            try:
                structure = ticket.input_module.ticket_category.organizational_structure
                obj_to_titulus_credential = get_credentials_class().objects.filter(
                    content_type=ContentType.objects.get_for_model(structure),
                    object_id=str(structure.pk)
                ).first()

                if not obj_to_titulus_credential:
                    logger.error(
                        f"[u:Titulus-Webhook] [{nrecord_ricevuto}] Credenziali Titulus non trovate")
                    return HttpResponse("Errore configurazione", status=500)

                # Chiamata a Titulus con le credenziali del gruppo recuperate.
                res = recupera_numero_protocollo(
                    obj_to_credential=obj_to_titulus_credential, 
                    nrecord=nrecord_ricevuto
                )

                if not res:
                    logger.error(
                        f"[u:Titulus-Webhook] [{nrecord_ricevuto}] Titulus non ha restituito il numero di protocollo per nrecord {nrecord_ricevuto}")
                    return HttpResponse("Errore recupero numero protocollo", status=500)

                with transaction.atomic():
                    ticket.protocol_number = res
                    ticket.protocol_date = timezone.localtime()
                    ticket.save(update_fields=[
                        "protocol_number",
                        "protocol_date"
                    ])
                    logger.info(
                        f"[u:Titulus-Webhook] Numero protocollo recuperato e aggiornato con successo nrecord {nrecord_ricevuto} protocollo {res} per ticket {ticket.code}")

            except Exception as e:
                logger.error(
                    f"[u:Titulus-Webhook] [{nrecord_ricevuto}] Errore recupero protocollo Titulus per nrecord {nrecord_ricevuto} e ticket {ticket.code}: {e}")
                return HttpResponse("Errore interno del server", status=500)
        # 3. Restituisci SEMPRE un 200 OK pulito, anche se l'nrecord non c'è o non ci sono documenti.
        # Questo evita che Titulus continui a martellare il tuo endpoint con retry infiniti.
        return HttpResponse("OK", status=200)

    # Se per qualche motivo chiamano con un metodo non supportato, restituisci 405
    return HttpResponse("Method Not Allowed", status=405)