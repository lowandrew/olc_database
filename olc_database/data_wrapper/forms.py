from django import forms
from dal import autocomplete
from django.forms.formsets import BaseFormSet
from data_wrapper.models import LSTSData, Sample, SeqData


def get_model_fields(model):
    fields = list()
    for field in model._meta.fields:
        field_id = str(field).split('.')[-1]
        fields.append(field_id)
    return fields


def make_list_of_fields():
    fields = list()
    for field in get_model_fields(LSTSData):
        if field not in fields:
            fields.append(field)
    for field in get_model_fields(SeqData):
        if field not in fields:
            fields.append(field)
    for field in get_model_fields(Sample):
        if field not in fields:
            fields.append(field)
    return fields


class SearchForm(forms.Form):
    OPERATION_CHOICES = (
        ('CONTAINS', 'CONTAINS'),
        ('DOES NOT CONTAIN', 'DOES NOT CONTAIN'),
        ('EQUALS', 'EQUALS'),
        ('DOES NOT EQUAL', 'DOES NOT EQUAL')
                         )

    AND_OR_CHOICES = (
        ('AND', 'AND'),
        ('OR', 'OR')
    )
    # search_attribute = forms.CharField(label='Search term', max_length=100)
    search_attribute = autocomplete.Select2ListChoiceField(choice_list=make_list_of_fields,
                                                           widget=autocomplete.ListSelect2(url='data_wrapper:attribute-autocomplete'))
    search_item = forms.CharField(label='Search term', max_length=100)
    operation = forms.ChoiceField(choices=OPERATION_CHOICES)
    combine_choice = forms.ChoiceField(choices=AND_OR_CHOICES)


class BaseSearchFormSet(BaseFormSet):
    def clean(self):
        """
        Does some stuff, as seen at http://whoisnicoleharris.com/2015/01/06/implementing-django-formsets.html
        I think that this is all I need to do. Remains to be seen.
        """
        if any(self.errors):
            return



