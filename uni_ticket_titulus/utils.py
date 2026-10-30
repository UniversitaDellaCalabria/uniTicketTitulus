from django.utils.module_loading import import_string
from .settings import *


def check_default_app_installed():
    return DEFAULT_TITULUS_APP in settings.INSTALLED_APPS

def get_credentials_class():
    if not check_default_app_installed(): return None
    return import_string(f"{DEFAULT_TITULUS_APP}.models.CredentialWSProtocollo")

def get_configuration_class():
    if not check_default_app_installed(): return None
    return import_string(f"{DEFAULT_TITULUS_APP}.models.ConfigurationWSProtocollo")

def get_configuration_op_class():
    if not check_default_app_installed(): return None
    return import_string(f"{DEFAULT_TITULUS_APP}.models.ConfigurationWSProtocolloOP")

def get_configuration_cc_class():
    if not check_default_app_installed(): return None
    return import_string(f"{DEFAULT_TITULUS_APP}.models.ConfigurationWSProtocolloCC")

def get_configuration_additional_config_class():
    if not check_default_app_installed(): return None
    return import_string(f"{DEFAULT_TITULUS_APP}.models.AdditionalConfigurationWSProtocollo")

def get_active_protocol_configuration(structure, category):
    if not (structure and category): return False

    credentials_ws_protocollo = get_credentials_class()
    configuration_ws_protocollo = get_configuration_class()

    if not (credentials_ws_protocollo and configuration_ws_protocollo): return False

    credentials = credentials_ws_protocollo.get_active_protocol_credential(structure)
    if not credentials: return False

    return configuration_ws_protocollo.get_active_protocol_configuration(category)

def protocolla(**kwargs):
    func = import_string(f"{DEFAULT_TITULUS_APP}.services.trova_ed_esegui_flusso_protocollo") 
    return func(**kwargs)

def recupera_numero_protocollo(**kwargs):
    func = import_string(f"{DEFAULT_TITULUS_APP}.services.recupera_numero_protocollo") 
    return func(**kwargs)