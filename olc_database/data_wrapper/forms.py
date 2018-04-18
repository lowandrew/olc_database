from django import forms
from django.forms.formsets import BaseFormSet


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
    search_attribute = forms.CharField(label='Search term', max_length=100)
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


