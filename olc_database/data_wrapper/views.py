from django.shortcuts import render
from data_wrapper.models import LSTSData, Sample, SeqData
from data_wrapper.forms import SearchForm, BaseSearchFormSet
from django.forms.formsets import formset_factory


# Create your views here.
def query_builder(request):
    terms = list()
    operations = list()
    attributes = list()
    SearchFormSet = formset_factory(SearchForm, formset=BaseSearchFormSet)
    if request.method == 'POST':
        search_formset = SearchFormSet(request.POST)
        if search_formset.is_valid():
            for search_form in search_formset:
                terms.append(search_form.cleaned_data.get('search_item'))
                attributes.append(search_form.cleaned_data.get('search_attribute'))
                operations.append(search_form.cleaned_data.get('operation'))
            print(attributes)
            print(operations)
            print(terms)
    else:
        search_formset = SearchFormSet()
    return render(request,
                  'data_wrapper/query_builder.html',
                  {
                      'search_formset': search_formset
                  },
                  )
