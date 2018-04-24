from django import forms
from dal import autocomplete
from django.forms.formsets import BaseFormSet
from data_wrapper.models import LSTSData, Sample, SeqData, ResFinderData


def get_model_fields(model):
    fields = list()
    for field in model._meta.fields:
        field_id = str(field).split('.')[-1]
        fields.append(field_id)
    return fields


def make_list_of_fields():
    fields = list()  # Would use a set here, but django-autocomplete-light wants a list.
    models = [Sample, SeqData, LSTSData, ResFinderData]
    for model in models:
        for field in get_model_fields(model):
            if field not in fields:
                fields.append(field)
    return fields


class ResFinderDataForm(forms.ModelForm):
    class Meta:
        model = ResFinderData
        fields = get_model_fields(ResFinderData)

    change_reason = forms.CharField(max_length=128)


class SeqDataForm(forms.ModelForm):
    class Meta:
        model = SeqData
        fields = get_model_fields(SeqData)

    change_reason = forms.CharField(max_length=128)


class SearchForm(forms.Form):
    OPERATION_CHOICES = (
        ('CONTAINS', 'CONTAINS'),
        # ('DOES NOT CONTAIN', 'DOES NOT CONTAIN'),
        ('EQUALS', 'EQUALS'),
        # ('DOES NOT EQUAL', 'DOES NOT EQUAL')  # TODO: Figure out how to implement these with the .filter
        ('LESS THAN', 'LESS THAN'),
        ('GREATER THAN', 'GREATER THAN'),
        ('BEFORE', 'BEFORE'),
        ('AFTER', 'AFTER'),
                         )

    AND_OR_CHOICES = (
        ('AND', 'AND'),
        # ('OR', 'OR')  # Also TODO: Add this in to the query builder once you figure out logic for it.
    )
    # search_attribute = forms.CharField(label='Search term', max_length=100)
    search_attribute = autocomplete.Select2ListChoiceField(choice_list=make_list_of_fields,
                                                           widget=autocomplete.ListSelect2(url='data_wrapper:attribute-autocomplete'),
                                                           required=True)
    search_item = forms.CharField(label='Search term', max_length=100, required=False)
    operation = forms.ChoiceField(choices=OPERATION_CHOICES,
                                  widget=forms.Select(attrs={
                                      'class': 'operation_choice'
                                  }))
    combine_choice = forms.ChoiceField(choices=AND_OR_CHOICES)
    date_input = forms.DateField(widget=forms.TextInput(attrs={
        'class': 'datepicker'
    }), required=False)


class QuerySaveForm(forms.Form):
    CHOICES = (('Yes', 'Yes'),
               ('No', 'No'))
    query_name = forms.CharField(max_length=256, required=False)  # This may be a bad idea. Change to True, maybe.
    save_query = forms.ChoiceField(choices=CHOICES,
                                   widget=forms.RadioSelect,
                                   initial='No')


class BaseSearchFormSet(BaseFormSet):
    def clean(self):
        """
        Does some stuff, as seen at http://whoisnicoleharris.com/2015/01/06/implementing-django-formsets.html
        I think that this is all I need to do. Remains to be seen.
        """
        if any(self.errors):
            return



