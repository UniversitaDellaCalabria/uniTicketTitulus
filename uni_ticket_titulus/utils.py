from django.utils.module_loading import import_string
from .settings import *


def check_default_app_installed():
    return TITULUS_APP in settings.INSTALLED_APPS

def get_credentials_class():
    if not check_default_app_installed(): return None
    return import_string(f"{TITULUS_APP}.models.{CREDENTIALS_CLASS}")

def get_configuration_class():
    if not check_default_app_installed(): return None
    return import_string(f"{TITULUS_APP}.models.{CONFIGURATION_CLASS}")

def get_configuration_op_class():
    if not check_default_app_installed(): return None
    return import_string(f"{TITULUS_APP}.models.{CONFIGURATION_OP_CLASS}")

def get_configuration_cc_class():
    if not check_default_app_installed(): return None
    return import_string(f"{TITULUS_APP}.models.{CONFIGURATION_CC_CLASS}")

def get_configuration_additional_config_class():
    if not check_default_app_installed(): return None
    return import_string(f"{TITULUS_APP}.models.{CONFIGURATION_ADDITIONAL_CLASS}")

def get_active_protocol_configuration(structure, category):
    if not (structure and category): return False

    credentials_ws_protocollo = get_credentials_class()
    configuration_ws_protocollo = get_configuration_class()

    if not (credentials_ws_protocollo and configuration_ws_protocollo): return False

    credentials = credentials_ws_protocollo.get_active_protocol_credential(structure)
    if not credentials: return False

    return configuration_ws_protocollo.get_active_protocol_configuration(category)

def protocolla(**kwargs):
    func = import_string(f"{TITULUS_APP}.services.{EXECUTE_FUNCTION}") 
    return func(**kwargs)

def recupera_numero_protocollo(**kwargs):
    func = import_string(f"{TITULUS_APP}.services.{GET_NUMBER_FUNCTION}") 
    return func(**kwargs)