import re
from django import forms
from dal import autocomplete
from django.forms.formsets import BaseFormSet
from data_wrapper.models import LSTSData, Sample, SeqData, ResFinderData, SeqTracking


def get_model_fields(model):
    fields = list()
    for field in model._meta.fields:
        field_id = str(field).split('.')[-1]
        fields.append(field_id)
    return fields


def make_list_of_fields():
    fields = list()  # Would use a set here, but django-autocomplete-light wants a list.
    models = [Sample, SeqData, LSTSData, ResFinderData, SeqTracking]
    for model in models:
        for field in get_model_fields(model):
            if field not in fields:
                fields.append(field)
    return fields


class SeqTrackingEditForm(forms.ModelForm):
    class Meta:
        model = SeqTracking
        fields = get_model_fields(SeqTracking)

    change_reason = forms.CharField(max_length=128)


class ResFinderDataForm(forms.ModelForm):
    class Meta:
        model = ResFinderData
        fields = get_model_fields(ResFinderData)

    change_reason = forms.CharField(max_length=128)


class SeqTrackingCreateForm(forms.Form):
    LOCATION_CHOICES = (
        ('BMH', 'BMH'),
        ('BUR', 'BUR'),
        ('CAL', 'CAL'),
        ('DAR', 'DAR'),
        ('GTA', 'GTA'),
        ('LON', 'LON'),
        ('MER', 'MER'),
        ('NML', 'NML'),
        ('OLC', 'OLC'),
        ('OLF', 'OLF'),
        ('OTT', 'OTT'),
        ('STH', 'STH')
    )
    PRIORITY_CHOICES = (
        ('IMMEDIATE', 'IMMEDIATE'),
        ('REAL-TIME', 'REAL-TIME'),
        ('RESEARCH', 'RESEARCH')
    )
    CURATOR_FLAG_CHOICES = (
        ('PASS', 'PASS'),
        ('REFERENCE', 'REFERENCE'),
        ('FAIL', 'FAIL'),
        ('QUANTIFIED', 'QUANTIFIED'),
        ('SEQUENCING', 'SEQUENCING'),
        ('SEQUENCED', 'SEQUENCED'),
        ('METAGENOME', 'METAGENOME'),
    )
    seqid = forms.CharField(max_length=128)
    lsts_id = forms.CharField(max_length=128)
    location = forms.ChoiceField(choices=LOCATION_CHOICES)
    oln_id = forms.CharField(max_length=128)
    project = forms.CharField(max_length=128)
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES)
    curator_flag = forms.ChoiceField(choices=CURATOR_FLAG_CHOICES)
    comment = forms.CharField(max_length=128, required=False)

    def clean_seqid(self):
        seqid = self.cleaned_data['seqid']
        if not re.match('\d{4}-[A-Z]+-\d{4}', seqid):
            raise forms.ValidationError('Invalid SEQID format. Correct format is YYYY-LAB-####')
        return seqid


class SeqDataForm(forms.ModelForm):
    class Meta:
        model = SeqData
        fields = get_model_fields(SeqData)

    change_reason = forms.CharField(max_length=128)


class CustomTableForm(forms.Form):
    table_attribute = autocomplete.Select2ListChoiceField(choice_list=make_list_of_fields,
                                                          widget=autocomplete.ListSelect2(url='data_wrapper:attribute-autocomplete'),
                                                          required=True)
    # Apparently when a form is completely blank in a formset, Django skips doing validation of it.
    # My hacky solution: Create another attribute to the form that defaults to a non-blank value, forcing
    # validation of the blank attribute. This hidden attribute is never displayed to the user.
    # A quick google didn't turn up a better way to solve the problem, but a better solution does probably exist.
    hidden_attribute = forms.CharField(max_length=1, required=False, empty_value='a')


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
        ('OR', 'OR')
    )
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
                                   initial='No')


class BaseSearchFormSet(BaseFormSet):
    def clean(self):
        """
        Does some stuff, as seen at http://whoisnicoleharris.com/2015/01/06/implementing-django-formsets.html
        I think that this is all I need to do. Remains to be seen.
        """
        if any(self.errors):
            return



