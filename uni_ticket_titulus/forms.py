from django import forms
from django.contrib.contenttypes.models import ContentType
from django.forms import inlineformset_factory, ModelForm
from django.utils.translation import gettext_lazy as _

from bootstrap_italia_template.widgets import (
    BootstrapItaliaSelectWidget,
)

from uni_ticket.settings import CLOSING_LEVELS
from uni_ticket_bootstrap_italia_template.widgets import UniTicketDateTimeWidget

from .utils import *


class OrganizationalStructureWSProtocolloModelForm(ModelForm):
    class Meta:
        model = get_credentials_class()
        fields = [
            "name",
            "protocollo_username",
            "protocollo_aoo",
            "protocollo_agd",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"disabled": True}),
            "protocollo_username": forms.TextInput(attrs={"disabled": True}),
            "protocollo_aoo": forms.TextInput(attrs={"disabled": True}),
            "protocollo_agd": forms.TextInput(attrs={"disabled": True}),
        }


class CategoryWSProtocolloForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.category = kwargs.pop("category")
        super().__init__(*args, **kwargs)
        fields_required = getattr(self.Meta, "fields_required", [])

        if fields_required:
            for key in self.fields:
                if key in fields_required:
                    self.fields[key].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.content_type = ContentType.objects.get_for_model(self.category)
        instance.object_id=str(self.category.pk)
        if commit:
            instance.save()
            self.save_m2m()
        return instance
    
    class Meta:
        model = get_configuration_class()
        fields = [
            "name",
            "protocollo_uo",
            "protocollo_cod_titolario",
            "protocollo_fascicolo_numero",
            # "protocollo_fascicolo_anno",
            "protocollo_uo_rpa",
            "protocollo_uo_rpa_username",
            "protocollo_uo_rpa_matricola",
            "protocollo_send_email",
        ]
        fields_required = [
            "protocollo_uo",
            'protocollo_cod_titolario',
            "protocollo_uo_rpa",
            "protocollo_uo_rpa_username",
            "protocollo_uo_rpa_matricola",
        ]
        labels = {
            "name": _("Denominazione configurazione"),
            "protocollo_uo": _("Unità Organizzativa"),
            "protocollo_uo_rpa": _("RPA Unità Organizzativa"),
            "protocollo_uo_rpa_username": _("Username RPA Unità Organizzativa"),
            "protocollo_uo_rpa_matricola": _("Matricola RPA Unità Organizzativa"),
            "protocollo_send_email": _("Invia e-mail a RPA"),
            "protocollo_email": _("Email riferimento"),
            "protocollo_cod_titolario": _("Titolario"),
            "protocollo_fascicolo_numero": _("Numero Fascicolo"),
            "protocollo_fascicolo_anno": _("Anno Fascicolo"),
        }
        help_texts = {
            "name": _('A discrezione dell\'utente. Es: "Configurazione anno 2020"'),
        }
        widgets = {
            "protocollo_cod_titolario": BootstrapItaliaSelectWidget,
            "protocollo_uo": BootstrapItaliaSelectWidget,
        }


class CategoryWSProtocolloDestinatarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields_required = getattr(self.Meta, "fields_required", [])

        if fields_required:
            for key in self.fields:
                if key in fields_required:
                    self.fields[key].required = True
                    
    class Meta:
        fields = [
            "protocollo_uo",
            "protocollo_persona",
            "protocollo_persona_username",
            "protocollo_persona_matricola",
        ]
        fields_required = [
            "protocollo_uo",
            'protocollo_persona',
            "protocollo_persona_username",
        ]


class CategoryWSProtocolloOPForm(CategoryWSProtocolloDestinatarioForm):
    class Meta(CategoryWSProtocolloDestinatarioForm.Meta):
        model = get_configuration_op_class()
        labels = {
            "protocollo_uo": _("UO"),
            "protocollo_persona": _("Nominativo"),
            "protocollo_persona_username": _("Username"),
            "protocollo_persona_matricola": _("Matricola"),
        }
    

CategoryWSProtocolloOPFormSet = inlineformset_factory(
    get_configuration_class(),
    get_configuration_op_class(),
    form=CategoryWSProtocolloOPForm,
    extra=0,
    max_num=1,
    validate_max=True,
    can_delete=True
)


class CategoryWSProtocolloCCForm(CategoryWSProtocolloDestinatarioForm):

    class Meta(CategoryWSProtocolloDestinatarioForm.Meta):
        model = get_configuration_cc_class()
        labels = {
            "protocollo_uo": _("UO CC"),
            "protocollo_persona": _("Nominativo CC"),
            "protocollo_persona_username": _("Username CC"),
            "protocollo_persona_matricola": _("Matricola CC"),
        }
        
CategoryWSProtocolloCCFormSet = inlineformset_factory(
    get_configuration_class(),
    get_configuration_cc_class(),
    form=CategoryWSProtocolloCCForm,
    extra=0,
    can_delete=True
)


class AdvancedConfigurationWSProtocolloForm(forms.ModelForm):
    # Definizione diretta con disabled=True
    # document_type = forms.CharField(initial="arrivo", disabled=True)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Imposta 'editor' come opzione selezionata di default
        self.fields['document_type'].initial = 'arrivo'
        self.fields['document_type'].disabled = True

    class Meta:
        model = get_configuration_additional_config_class()
        fields = [
            "document_type",
            "iter",
        ]
        labels = {
            "document_type": _("Tipo"),
            "iter": _("Iter"),
        }
