from django.conf import settings


# default values
TITULUS_APP = getattr(settings, "DEFAULT_TITULUS_APP", "titulus_utility")

CREDENTIALS_CLASS = "CredentialWSProtocollo"
CONFIGURATION_CLASS = "ConfigurationWSProtocollo"
CONFIGURATION_OP_CLASS ="ConfigurationWSProtocolloOP"
CONFIGURATION_CC_CLASS ="ConfigurationWSProtocolloCC"
CONFIGURATION_ADDITIONAL_CLASS ="AdditionalConfigurationWSProtocollo"

EXECUTE_FUNCTION = "trova_ed_esegui_flusso_protocollo"
GET_NUMBER_FUNCTION = "recupera_numero_protocollo"

# in settingslocal.py
# generazione
# import secrets
# return secrets.token_hex(32)
# TITULUS_NOTIFICATION_AUTH='your_auth_token'