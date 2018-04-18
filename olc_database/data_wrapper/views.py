from django.shortcuts import render
from data_wrapper.models import LSTSData, Sample, SeqData
from data_wrapper.forms import SearchForm, BaseSearchFormSet
from django.forms.formsets import formset_factory


# Create your views here.
def query_builder(request):
    terms = list()
    operations = list()
    attributes = list()
    combine_operations = list()
    SearchFormSet = formset_factory(SearchForm, formset=BaseSearchFormSet)
    acceptable_fields = make_set_of_fields()
    print(acceptable_fields)
    if request.method == 'POST':
        search_formset = SearchFormSet(request.POST)
        if search_formset.is_valid():
            for search_form in search_formset:
                terms.append(search_form.cleaned_data.get('search_item'))
                attributes.append(search_form.cleaned_data.get('search_attribute'))
                operations.append(search_form.cleaned_data.get('operation'))
                combine_operations.append(search_form.cleaned_data.get('combine_choice'))
            print(attributes)
            print(operations)
            print(terms)
            print(combine_operations)
    else:
        search_formset = SearchFormSet()
    return render(request,
                  'data_wrapper/query_builder.html',
                  {
                      'search_formset': search_formset
                  },
                  )


# These should most likely end up not in my view eventually.
def get_model_fields(model):
    fields = list()
    for field in model._meta.fields:
        field_id = str(field).split('.')[-1]
        fields.append(field_id)
    return fields


def make_set_of_fields():
    fields = set()
    for field in get_model_fields(LSTSData):
        fields.add(field)
    for field in get_model_fields(SeqData):
        fields.add(field)
    for field in get_model_fields(Sample):
        fields.add(field)
    return fields
