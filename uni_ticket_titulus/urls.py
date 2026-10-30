from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import path, re_path
from django.utils.text import slugify
from django.views.generic import RedirectView

from uni_ticket.decorators import is_manager, is_operator, is_super_admin, is_the_owner
from uni_ticket.settings import MANAGEMENT_URL_PREFIX
from uni_ticket.urls import base, category_id

from .views import manager, generic


app_name = "uni_ticket_titulus"


structure_protocol_configurations = "{}/settings/protocol-configurations".format(
    base)
structure_protocol_configuration = "{}/<int:configuration_id>".format(
    structure_protocol_configurations
)

category_protocol_configurations = "{}/protocol-configurations".format(
    category_id)
category_protocol_configuration = "{}/<int:configuration_id>".format(
    category_protocol_configurations
)

urlpatterns = [
    # Structure Protocol configurations
    path(
        "{}/".format(structure_protocol_configuration),
        manager.structure_protocol_configuration_detail,
        name="manager_structure_protocol_configuration_detail",
    ),
    # Category Protocol configurations
    path(
        "{}/".format(category_protocol_configuration),
        manager.category_protocol_configuration_detail,
        name="manager_category_protocol_configuration_detail",
    ),
    path(
        "{}/new/".format(category_protocol_configurations),
        manager.category_protocol_configuration_new,
        name="manager_category_protocol_configuration_new",
    ),
    path(
        "{}/delete/".format(category_protocol_configuration),
        manager.category_protocol_configuration_delete,
        name="manager_category_protocol_configuration_delete",
    ),
    path(
        "{}/disable/".format(category_protocol_configuration),
        manager.category_protocol_configuration_disable,
        name="manager_category_protocol_configuration_disable",
    ),
    path(
        "{}/enable/".format(category_protocol_configuration),
        manager.category_protocol_configuration_enable,
        name="manager_category_protocol_configuration_enable",
    ),
    path(
        'endpoint_titulus_webhook/', 
        generic.endpoint_titulus_webhook, 
        name='endpoint_titulus_webhook'
    ),
]
