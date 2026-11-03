from django.db.models.signals import *
from django.dispatch import receiver

from organizational_area.decorators import disable_for_loaddata

from uni_ticket.models import TicketCategory

from .utils import *


@receiver(pre_save, sender=get_credentials_class())
@disable_for_loaddata
def structure_conf_disable_categories_protocol_flag_pre_save(sender, instance, **kwargs):
    """
    If an active structure configuration is disabled,
    all categories with flag checked must be updated
    """

    # if not new object
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.is_active and not instance.is_active:
            TicketCategory.objects.filter(
                organizational_structure__pk=instance.object_id,
                protocol_required=True
            ).update(
                protocol_required=False
            )


@receiver(pre_delete, sender=get_credentials_class())
@disable_for_loaddata
def structure_conf_disable_categories_protocol_flag_pre_delete(sender, instance, **kwargs):
    """
    If an active structure configuration is deleted,
    all categories with flag checked must be updated
    """
    if instance.is_active:
        TicketCategory.objects.filter(
            organizational_structure__pk=instance.object_id,
            protocol_required=True
        ).update(
            protocol_required=False
        )


@receiver(pre_save, sender=get_configuration_class())
@disable_for_loaddata
def category_conf_disable_categories_protocol_flag_save(sender, instance, **kwargs):
    """
    If an active category configuration is disabled,
    category must be updated with false check
    """

    # if not new object
    if instance.pk:
        old_instance = sender.objects.get(pk=instance.pk)
        if old_instance.is_active and not instance.is_active:
            ticket_category = TicketCategory.objects.filter(
                pk=instance.object_id
            ).first()
            if ticket_category:
                ticket_category.protocol_required = False
                ticket_category.save()


@receiver(pre_delete, sender=get_configuration_class())
@disable_for_loaddata
def category_conf_disable_categories_protocol_flag_delete(sender, instance, **kwargs):
    """
    If an active category configuration is deleted,
    category must be updated with false check
    """
    if instance.is_active:
        ticket_category = TicketCategory.objects.filter(
            pk=instance.object_id
        ).first()
        if ticket_category:
            ticket_category.protocol_required = False
            ticket_category.save()