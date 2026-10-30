import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from django_form_builder.utils import get_labeled_errors
from organizational_area.models import *

from uni_ticket.decorators import is_manager
from uni_ticket.models import *
from uni_ticket.utils import (
    base_context,
)

from ..forms import *
from ..utils import *

logger = logging.getLogger(__name__)


@login_required
@is_manager
def structure_protocol_configuration_detail(
    request, structure_slug, configuration_id
):
    """
    Structure protocol configuration details

    :type structure_slug: String
    :type configuration_id: Integer

    :param structure_slug: structure slug
    :param configuration_id: protocol configuration pk

    :return: response
    """
    # from @is_manager
    structure = request.structure

    configuration = get_object_or_404(
        get_credentials_class(),
        content_type=ContentType.objects.get_for_model(structure),
        object_id=str(structure.pk),
        pk=configuration_id,
    )

    template = "protocol/structure_protocol_configuration.html"
    title = _("Configurazione protocollo informatico")

    form = OrganizationalStructureWSProtocolloModelForm(instance=configuration)

    # POST ACTION DISABLED
    # FORM FIELDS DISABLED
    # if request.method == 'POST':
    # form = OrganizationalStructureWSProtocolloModelForm(instance=configuration,
    # data=request.POST)
    # if form.is_valid():
    # configuration = form.save(commit=False)
    # if not configuration.protocollo_email:
    # configuration.protocollo_email = settings.PROTOCOL_EMAIL_DEFAULT
    # configuration.save()

    # messages.add_message(request, messages.SUCCESS,
    # _("Configurazione protocollo informatico aggiornata"))
    # return redirect('uni_ticket:manager_structure_protocol_configuration_detail',
    # structure_slug=structure_slug,
    # configuration_id=configuration.pk)
    # else:
    # for k,v in get_labeled_errors(form).items():
    # messages.add_message(request, messages.ERROR,
    # "<b>{}</b>: {}".format(k, strip_tags(v)))
    d = {
        "configuration": configuration,
        "form": form,
        "structure": structure,
        "sub_title": structure,
        "title": title,
    }
    response = render(request, template, base_context(d))
    return response


@login_required
@is_manager
def category_protocol_configuration_detail(
    request, structure_slug, category_slug, configuration_id
):
    """
    Category protocol configuration detail

    :type structure_slug: String
    :type category_slug: String
    :type configuration_id: Integer

    :param structure_slug: structure slug
    :param category_slug: category slug
    :param configuration_id: protocol configuration pk

    :return: response
    """
    # from @is_manager
    structure = request.structure

    category = get_object_or_404(
        TicketCategory, organizational_structure=structure, slug=category_slug
    )
    configuration = get_object_or_404(
        get_configuration_class(),
        pk=configuration_id,
        content_type=ContentType.objects.get_for_model(category),
        object_id=str(category.pk)
    )

    additional_configuration = get_configuration_additional_config_class().objects.filter(
        configurator=configuration
    ).first()

    template = "protocol/category_protocol_configuration_detail.html"
    title = _("Configurazione protocollo informatico")

    form = CategoryWSProtocolloForm(
        category=category, 
        instance=configuration
    )
    formset_op = CategoryWSProtocolloOPFormSet(prefix="op", instance=configuration)
    formset_cc = CategoryWSProtocolloCCFormSet(prefix="cc", instance=configuration)
    form_advanced_conf = AdvancedConfigurationWSProtocolloForm(instance=additional_configuration)
    
    if request.method == "POST":
        form = CategoryWSProtocolloForm(
            category=category, 
            instance=configuration, 
            data=request.POST
        )
        formset_op = CategoryWSProtocolloOPFormSet(
            prefix="op",
            data=request.POST,
            instance=configuration
        )
        formset_cc = CategoryWSProtocolloCCFormSet(
            prefix="cc",
            data=request.POST,
            instance=configuration
        )
        form_advanced_conf = AdvancedConfigurationWSProtocolloForm(
            data=request.POST,
            instance=additional_configuration
        )
        if form.is_valid() and formset_op.is_valid() and formset_cc.is_valid():
            form.save()
            formset_op.save()
            formset_cc.save()
            
            adv = form_advanced_conf.save(commit=False)
            adv.configurator = configuration
            adv.save()

            messages.add_message(
                request,
                messages.SUCCESS,
                _("Configurazione protocollo informatico aggiornata"),
            )
            return redirect(
                "uni_ticket_titulus:manager_category_protocol_configuration_detail",
                structure_slug=structure_slug,
                category_slug=category_slug,
                configuration_id=configuration.pk,
            )
        else:
            for k, v in get_labeled_errors(form).items():
                messages.add_message(
                    request, messages.ERROR, "<b>{}</b>: {}".format(k, strip_tags(v))
                )
            if formset_op.errors:
                messages.add_message(
                    request, messages.ERROR, _("Correggi gli errori nell'operatore destinatario")
                )
            if formset_cc.errors:
                messages.add_message(
                    request, messages.ERROR, _("Correggi gli errori nei destinatari CC")
                )
    d = {
        "category": category,
        "configuration": configuration,
        "form": form,
        "formset_op": formset_op,
        "formset_cc": formset_cc,
        "form_advanced_conf": form_advanced_conf,
        "structure": structure,
        "sub_title": category,
        "title": title,
    }
    response = render(request, template, base_context(d))
    return response


@login_required
@is_manager
def category_protocol_configuration_new(
    request, structure_slug, category_slug
):
    """
    Creates a new protocol configuration for category

    :type structure_slug: String
    :type category_slug: String

    :param structure_slug: structure slug
    :param category_slug: category slug

    :return: render
    """
    # from @is_manager
    structure = request.structure

    title = _("Nuova configuratione del protocollo informatico")
    category = get_object_or_404(
        TicketCategory, organizational_structure=structure, slug=category_slug
    )
    form = CategoryWSProtocolloForm(category=category)
    formset_op = CategoryWSProtocolloOPFormSet(prefix="op")
    formset_cc = CategoryWSProtocolloCCFormSet(prefix="cc")
    form_advanced_conf = AdvancedConfigurationWSProtocolloForm()

    if request.method == "POST":
        form = CategoryWSProtocolloForm(
            category=category,
            data=request.POST
        )
        formset_op = CategoryWSProtocolloOPFormSet(
            prefix="op", data=request.POST,
        )
        formset_cc = CategoryWSProtocolloCCFormSet(
            prefix="cc", data=request.POST,
        )
        form_advanced_conf = AdvancedConfigurationWSProtocolloForm(
            data=request.POST,
        )
        if form.is_valid() and formset_op.is_valid() and formset_cc.is_valid():
            configuration = form.save(commit=False)
            configuration.ticket_category = category
            configuration.save()
            formset_op.save()
            formset_cc.save()

            adv = form_advanced_conf.save(commit=False)
            adv.configurator = configuration
            form_advanced_conf.save()

            # log action
            logger.info(
                "[{}] manager of structure {}"
                " {} created the new protocol configuration {}"
                " for category {}".format(
                    timezone.localtime(),
                    structure,
                    request.user,
                    configuration,
                    category,
                )
            )

            messages.add_message(
                request, messages.SUCCESS, _("Configurazione creata con successo")
            )

            return redirect(
                "uni_ticket_titulus:manager_category_protocol_configuration_detail",
                structure_slug=structure_slug,
                category_slug=category_slug,
                configuration_id=configuration.pk,
            )
        else:
            for k, v in get_labeled_errors(form).items():
                messages.add_message(
                    request, messages.ERROR, "<b>{}</b>: {}".format(k, strip_tags(v))
                )
            if formset_op.errors:
                messages.add_message(
                    request, messages.ERROR, _("Correggi gli errori nell'operatore destinatario")
                )
            if formset_cc.errors:
                messages.add_message(
                    request, messages.ERROR, _("Correggi gli errori nei destinatari CC")
                )

    template = "protocol/category_protocol_configuration_new.html"
    d = {
        "category": category,
        "form": form,
        "formset_op": formset_op,
        "formset_cc": formset_cc,
        "form_advanced_conf": form_advanced_conf,
        "structure": structure,
        "sub_title": category,
        "title": title,
    }
    return render(request, template, base_context(d))


@require_POST
@login_required
@is_manager
def category_protocol_configuration_delete(
    request, structure_slug, category_slug, configuration_id
):
    """
    Deletes a category protocol configuration

    :type structure_slug: String
    :type category_slug: String
    :type configuration_id: Integer

    :param structure_slug: structure slug
    :param category_slug: category slug
    :param configuration_id: protocol configuration pk

    :return: redirect
    """
    # from @is_manager
    structure = request.structure

    category = get_object_or_404(
        TicketCategory, organizational_structure=structure, slug=category_slug
    )

    configuration = get_object_or_404(
        get_configuration_class(),
        pk=configuration_id,
        content_type=ContentType.objects.get_for_model(category),
        object_id=str(category.pk)
    )

    if not get_active_protocol_configuration(
        structure=structure,
        category=category
    ):
        category.protocol_required = False
        category.save(update_fields=["protocol_required", "modified"])
        messages.add_message(
            request,
            messages.INFO,
            _(
                "Nessuna configurazione di protocollo "
                "valida per la tipologia. "
                "Protocollo obbligatorio disabilitato."
                ""
            ).format(category),
        )

    messages.add_message(
        request,
        messages.SUCCESS,
        _("Configurazione <b>{}</b> eliminata correttamente").format(configuration),
    )
    configuration.delete()
    return redirect(
        "uni_ticket:manager_category_detail",
        structure_slug=structure_slug,
        category_slug=category_slug,
    )


@require_POST
@login_required
@is_manager
def category_protocol_configuration_disable(
    request, structure_slug, category_slug, configuration_id
):
    """
    Disables a category protocol configuration

    :type structure_slug: String
    :type category_slug: String
    :type configuration_id: Integer

    :param structure_slug: structure slug
    :param category_slug: category slug
    :param configuration_id: protocol configuration pk

    :return: redirect
    """
    # from @is_manager
    structure = request.structure

    category = get_object_or_404(
        TicketCategory, organizational_structure=structure, slug=category_slug
    )
    configuration = get_object_or_404(
        get_configuration_class(),
        pk=configuration_id,
        content_type=ContentType.objects.get_for_model(category),
        object_id=str(category.pk)
    )
    
    if configuration.is_active:
        configuration.is_active = False
        configuration.save(update_fields=["is_active", "modified"])

        category.protocol_required = False
        category.save(update_fields=["protocol_required", "modified"])

        # signal active here to disable category protocol flag

        messages.add_message(
            request,
            messages.SUCCESS,
            _("Configurazione <b>{}</b> disattivata con successo").format(
                configuration
            ),
        )
        messages.add_message(
            request,
            messages.INFO,
            _(
                "Nessuna configurazione di protocollo "
                "valida per la tipologia. "
                "Protocollo obbligatorio disabilitato."
                ""
            ).format(category),
        )

        # log action
        logger.info(
            "[{}] manager of structure {}"
            " {} disabled the category {} protocol configuration {}"
            "".format(
                timezone.localtime(), structure, request.user, category, configuration
            )
        )
    else:
        messages.add_message(
            request,
            messages.ERROR,
            _("Configurazione {} già disattivata").format(configuration),
        )

    return redirect(
        "uni_ticket:manager_category_detail",
        structure_slug=structure_slug,
        category_slug=category_slug,
    )


@require_POST
@login_required
@is_manager
def category_protocol_configuration_enable(
    request, structure_slug, category_slug, configuration_id
):
    """
    Enables a category protocol configuration

    :type structure_slug: String
    :type category_slug: String
    :type configuration_id: Integer

    :param structure_slug: structure slug
    :param category_slug: category slug
    :param configuration_id: protocol configuration pk

    :return: redirect
    """
    # from @is_manager
    structure = request.structure

    category = get_object_or_404(
        TicketCategory, organizational_structure=structure, slug=category_slug
    )
    configuration = get_object_or_404(
        get_configuration_class(),
        pk=configuration_id,
        content_type=ContentType.objects.get_for_model(category),
        object_id=str(category.pk)
    )

    if configuration.is_active:
        messages.add_message(
            request,
            messages.ERROR,
            _("Configurazione {} già attivata").format(configuration),
        )

    else:
        configuration.is_active = True
        configuration.save(update_fields=["is_active", "modified"])

        # only one
        # MADE BY SIGNAL!
        # configuration.disable_other_configurations()

        messages.add_message(
            request,
            messages.SUCCESS,
            _("Configurazione <b>{}</b> attivata con successo").format(configuration),
        )

        # log action
        logger.info(
            "[{}] manager of structure {}"
            " {} enabled the category {} protocol configuration {}"
            "".format(
                timezone.localtime(), structure, request.user, category, configuration
            )
        )

    return redirect(
        "uni_ticket:manager_category_detail",
        structure_slug=structure_slug,
        category_slug=category_slug,
    )
