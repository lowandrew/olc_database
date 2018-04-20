from dal import autocomplete
from django.shortcuts import render
from data_wrapper.models import LSTSData, Sample, SeqData
from .forms import SearchForm, BaseSearchFormSet
from django.forms.formsets import formset_factory


class AttributeAutocompleteFromList(autocomplete.Select2ListView):
    def get_list(self):
        return make_list_of_fields()


# Create your views here.
def query_builder(request):
    terms = list()
    operations = list()
    attributes = list()
    combine_operations = list()
    SearchFormSet = formset_factory(SearchForm, formset=BaseSearchFormSet)
    if request.method == 'POST':
        search_formset = SearchFormSet(request.POST)
        if search_formset.is_valid():
            for search_form in search_formset:
                if search_form.cleaned_data.get('date_input'):
                    terms.append(search_form.cleaned_data.get('date_input'))
                else:
                    terms.append(search_form.cleaned_data.get('search_item'))
                attributes.append(search_form.cleaned_data.get('search_attribute'))
                operations.append(search_form.cleaned_data.get('operation'))
                combine_operations.append(search_form.cleaned_data.get('combine_choice'))
            seqids = decipher_input_request(attributes, operations, terms, combine_operations)
            if len(seqids) == 1 and 'ERROR' in seqids[0]:
                return render(request,
                              'data_wrapper/query_builder.html',
                              {
                                 'search_formset': search_formset,
                                 'error_msg': seqids[0]
                              })
            else:
                return render(request,
                              'data_wrapper/query_results.html',
                              {
                                  'seqids': seqids
                              })

    else:
        search_formset = SearchFormSet()
    return render(request,
                  'data_wrapper/query_builder.html',
                  {
                      'search_formset': search_formset
                  },
                  )


def query_results(request):
    return render(request,
                  'data_wrapper/query_results.html')


def decipher_input_request(attributes, operations, terms, combine_operations):
    # NOTE: This may not be a good way to do things at all, but as a proof of concept it seems to work.
    # TODO: Become a database expert so you know if this is actually a good idea.
    samples = Sample.objects.all()
    for i in range(len(attributes)):
        # Step 1: Find which model/field we're pulling stuff from.
        if attributes[i] in get_model_fields(LSTSData):
            model = LSTSData
            field = model._meta.get_field(attributes[i])
        elif attributes[i] in get_model_fields(SeqData):
            model = SeqData
            field = model._meta.get_field(attributes[i])

        queryset = model.objects.all()
        fieldname = str(field).split('.')[-1]
        # With that done, do different things depending on the operation.
        if operations[i] == 'EQUALS':
            # This is some black magic that allows strings to be passed as keyword arguments. I had no idea this was
            # a thing that was possible until today.
            queryset = queryset.filter(**{fieldname + '__iexact': terms[i]})
        elif operations[i] == 'CONTAINS':
            queryset = queryset.filter(**{fieldname + '__icontains': terms[i]})
        elif operations[i] == 'GREATER THAN':
            # Make sure user has entered an int. If they haven't, they'll get told that they messed up with a nice
            # error message.
            try:
                term_as_integer = int(terms[i])
            except ValueError:
                return ['ERROR: When using a greater than or less than operation, you must enter a number.'
                        ' Please try again.']
            queryset = queryset.filter(**{fieldname + '__gt': term_as_integer})
        elif operations[i] == 'LESS THAN':
            try:
                term_as_integer = int(terms[i])
            except ValueError:
                return ['ERROR: When using a greater than or less than operation, you must enter a number.'
                        ' Please try again.']
            queryset = queryset.filter(**{fieldname + '__lt': term_as_integer})
        elif operations[i] == 'BEFORE':
            queryset = queryset.filter(**{fieldname + '__date__lt': terms[i]})
        elif operations[i] == 'AFTER':
            queryset = queryset.filter(**{fieldname + '__date__gt': terms[i]})

        queryset_seqids = list()
        for item in queryset:
            queryset_seqids.append(str(item.seqid))
        for sample in samples:
            if sample.seqid not in queryset_seqids:
                samples = samples.exclude(seqid=sample.seqid)

    seqids = list()
    for sample in samples:
        seqids.append(sample.seqid)
    return seqids


def get_model_fields(model):
    fields = list()
    for field in model._meta.fields:
        field_id = str(field).split('.')[-1]
        fields.append(field_id)
    return fields


def make_list_of_fields():
    fields = list()  # Would use a set here, but django-autocomplete-light wants a list.
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

