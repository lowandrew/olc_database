from dal import autocomplete
from django_tables2 import RequestConfig
from django.shortcuts import render, get_object_or_404, redirect
from data_wrapper.models import LSTSData, Sample, SeqData, ResFinderData, SavedQueries
from .forms import SearchForm, BaseSearchFormSet, QuerySaveForm
from .tables import SeqDataTable
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required


class AttributeAutocompleteFromList(autocomplete.Select2ListView):
    def get_list(self):
        return make_list_of_fields()


# Create your views here.
@login_required
def query_builder(request):
    terms = list()
    operations = list()
    attributes = list()
    combine_operations = list()
    SearchFormSet = formset_factory(SearchForm, formset=BaseSearchFormSet)
    save_query_form = QuerySaveForm()
    if request.method == 'POST':
        save_query_form = QuerySaveForm(request.POST)
        query_name = ''
        save_query = 'No'
        if save_query_form.is_valid():
            query_name = save_query_form.cleaned_data.get('query_name')
            save_query = save_query_form.cleaned_data.get('save_query')
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
                                 'error_msg': seqids[0],
                                 'save_query_form': save_query_form
                              })
            else:
                if save_query == 'Yes':
                    SavedQueries.objects.create(user=request.user,
                                                search_terms=terms,
                                                search_attributes=attributes,
                                                search_operations=operations,
                                                search_combine_operations=combine_operations,
                                                query_name=query_name)
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
                      'search_formset': search_formset,
                      'save_query_form': save_query_form
                  },
                  )


@login_required
def saved_queries(request):
    saved_queries = SavedQueries.objects.filter(user=request.user)
    return render(request,
                  'data_wrapper/saved_queries.html',
                  {'saved_queries': saved_queries}
                  )


@login_required
def delete_query_confirm(request, query_id):
    query = get_object_or_404(SavedQueries, pk=query_id)
    return render(request,
                  'data_wrapper/delete_query_confirm.html',
                  {
                      'query': query
                  }
                  )


@login_required
def delete_query(request, query_id):
    query = get_object_or_404(SavedQueries, pk=query_id)
    query.delete()
    return redirect('data_wrapper:saved_queries')


@login_required
def rerun_query(request, query_id):
    query = get_object_or_404(SavedQueries, pk=query_id)
    seqids = decipher_input_request(attributes=query.search_attributes,
                                    operations=query.search_operations,
                                    terms=query.search_terms,
                                    combine_operations=query.search_combine_operations)
    return render(request,
                  'data_wrapper/query_results.html',
                  {
                      'seqids': seqids
                  })

@login_required
def query_details(request, query_id):
    query = get_object_or_404(SavedQueries, pk=query_id)
    return render(request,
                  'data_wrapper/query_details.html',
                  {
                      'query': query
                  })

def query_results(request):
    return render(request,
                  'data_wrapper/query_results.html')


def seqdata_table(request):
    table = SeqDataTable(SeqData.objects.all())
    RequestConfig(request).configure(table)
    return render(request,
                  'data_wrapper/seqdata_table.html',
                  {
                      'table': table
                  })


def decipher_input_request(attributes, operations, terms, combine_operations):
    # NOTE: This may not be a good way to do things at all, but as a proof of concept it seems to work.
    # TODO: Become a database expert so you know if this is actually a good idea.
    samples = Sample.objects.all()
    models = [Sample, SeqData, LSTSData, ResFinderData]
    for i in range(len(attributes)):
        # Step 1: Find which model/field we're pulling stuff from.
        for m in models:
            if attributes[i] in get_model_fields(m):
                model = m
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
    models = [Sample, SeqData, LSTSData, ResFinderData]
    for model in models:
        for field in get_model_fields(model):
            if field not in fields:
                fields.append(field)
    return fields

