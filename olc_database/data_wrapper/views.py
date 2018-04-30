from dal import autocomplete
from django_tables2 import RequestConfig
from django_tables2.columns import TemplateColumn
from django.shortcuts import render, get_object_or_404, redirect
from data_wrapper.models import LSTSData, Sample, SeqData, ResFinderData, SavedQueries, SavedTables, SeqIdList, SeqTracking
from .forms import SearchForm, BaseSearchFormSet, QuerySaveForm, ResFinderDataForm, SeqDataForm, CustomTableForm, \
    SeqTrackingCreateForm, SeqTrackingEditForm
from .tables import SeqDataTable, ResFinderDataTable, SeqTrackingTable
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# This view is needed to make autocomplete for table/query builder work.
class AttributeAutocompleteFromList(autocomplete.Select2ListView):
    def get_list(self):
        return make_list_of_fields()


# Create your views here.
@login_required
def table_builder(request):
    terms = list()
    TableFormSet = formset_factory(CustomTableForm, formset=BaseSearchFormSet)
    save_query_form = QuerySaveForm()
    if request.method == 'POST':
        save_query_form = QuerySaveForm(request.POST)
        query_name = ''
        save_query = 'No'
        if save_query_form.is_valid():
            query_name = save_query_form.cleaned_data.get('query_name')
            save_query = save_query_form.cleaned_data.get('save_query')
        table_formset = TableFormSet(request.POST)
        if table_formset.is_valid():
            for table_form in table_formset:
                terms.append(table_form.cleaned_data.get('table_attribute'))
            seqid_list = list(Sample.objects.values_list('seqid', flat=True))
            table_data = get_table_data(table_attributes=terms,
                                        seqid_list=seqid_list)
            if save_query == 'Yes':
                SavedTables.objects.create(user=request.user,
                                           table_attributes=terms,
                                           table_name=query_name)
            terms.insert(0, 'SEQID')
            return render(request,
                          'data_wrapper/generic_table.html',
                          {
                              'table_data': table_data,
                              'table_attributes': terms
                          })

    else:
        table_formset = TableFormSet()
    return render(request,
                  'data_wrapper/table_builder.html',
                  {
                      'table_formset': table_formset,
                      'save_query_form': save_query_form
                  })


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
                saved_tables = SavedTables.objects.filter(user=request.user)
                seqid_object = SeqIdList.objects.create(seqid_list=seqids)
                return render(request,
                              'data_wrapper/query_results.html',
                              {
                                  'seqids': seqids,
                                  'saved_tables': saved_tables,
                                  'seqid_id': seqid_object.pk
                              })
        else:
            return render(request,
                          'data_wrapper/query_builder.html',
                          {
                              'search_formset': search_formset,
                              'save_query_form': save_query_form
                          },
                          )
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
                  {'saved_queries': saved_queries,
                   }
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
def delete_table_confirm(request, table_id):
    table = get_object_or_404(SavedTables, pk=table_id)
    return render(request,
                  'data_wrapper/delete_table_confirm.html',
                  {
                      'table': table
                  }
                  )


@login_required
def delete_table(request, table_id):
    table = get_object_or_404(SavedTables, pk=table_id)
    table.delete()
    return redirect('data_wrapper:saved_queries')


@login_required
def edit_data_resfinder(request, resfinder_id):
    resfinder_data = get_object_or_404(ResFinderData, pk=resfinder_id)
    resfinder_form = ResFinderDataForm(instance=resfinder_data)
    if request.method == 'POST':
        resfinder_form = ResFinderDataForm(request.POST)
        if resfinder_form.is_valid():
            r = ResFinderDataForm(request.POST, instance=resfinder_data)
            change_reason = resfinder_form.cleaned_data.get('change_reason')
            with_reason = r.save(commit=False)
            with_reason.changeReason = change_reason
            r.save()
            return redirect('data_wrapper:resfinderdata_table')
    else:
        return render(request,
                      'data_wrapper/edit_data_resfinder.html',
                      {'resfinder_form': resfinder_form},
                      )


@login_required
def edit_data_seqdata(request, seqdata_id):
    seqdata = get_object_or_404(SeqData, pk=seqdata_id)
    seqdata_form = SeqDataForm(instance=seqdata)
    if request.method == 'POST':
        seqdata_form = SeqDataForm(request.POST)
        if seqdata_form.is_valid():
            # Have to do some fancy footwork here to make the change reason save with the other form data.
            # Not entirely sure how this works, but it does, so I won't complain.
            s = SeqDataForm(request.POST, instance=seqdata)
            change_reason = seqdata_form.cleaned_data.get('change_reason')
            with_reason = s.save(commit=False)
            with_reason.changeReason = change_reason
            s.save()
            return redirect('data_wrapper:seqdata_table')
    else:
        return render(request,
                      'data_wrapper/edit_data_seqdata.html',
                      {'seqdata_form': seqdata_form},
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
    seqid_object = SeqIdList.objects.create(seqid_list=seqids)
    saved_tables = SavedTables.objects.filter(user=request.user)
    return render(request,
                  'data_wrapper/query_results.html',
                  {
                      'seqids': seqids,
                      'saved_tables': saved_tables,
                      'seqid_id': seqid_object.pk
                  })


@login_required
def query_details(request, query_id):
    query = get_object_or_404(SavedQueries, pk=query_id)
    query_detail_list = list()
    for i in range(len(query.search_terms)):
        if i < len(query.search_terms) - 1:
            if query.search_combine_operations[i] == 'OR':
                query_detail_list.append(query.search_attributes[i] + ' ' + query.search_operations[i] +
                                         ' ' + query.search_terms[i])
                query_detail_list.append(query.search_combine_operations[i])
            else:
                query_detail_list.append(query.search_attributes[i] + ' ' + query.search_operations[i] +
                                         ' ' + query.search_terms[i] + ' ' + query.search_combine_operations[i])
        else:
            query_detail_list.append(query.search_attributes[i] + ' ' + query.search_operations[i] +
                                     ' ' + query.search_terms[i])
    return render(request,
                  'data_wrapper/query_details.html',
                  {
                      'query': query,
                      'query_detail_list': query_detail_list
                  })


@login_required
def seqdata_history(request, seqdata_id):
    seqdata = get_object_or_404(SeqData, pk=seqdata_id)
    histories = seqdata.history.all()
    table = SeqDataTable(histories,
                         extra_columns=[('Date Changed', TemplateColumn('{{ record.history_date }}')),
                                        ('Changed By', TemplateColumn('{{ record.history_user }}')),
                                        ('Change Reason', TemplateColumn('{{ record.history_change_reason }}'))])
    RequestConfig(request).configure(table)
    return render(request,
                  'data_wrapper/seqdata_history.html',
                  {
                      'seqdata': seqdata,
                      'table': table,
                  })


@login_required
def resfinder_history(request, resfinder_id):
    resfinderdata = get_object_or_404(ResFinderData, pk=resfinder_id)
    histories = resfinderdata.history.all()
    table = ResFinderDataTable(histories,
                               extra_columns=[('Date Changed', TemplateColumn('{{ record.history_date }}')),
                                              ('Changed By', TemplateColumn('{{ record.history_user }}')),
                                              ('Change Reason', TemplateColumn('{{ record.history_change_reason }}'))])
    RequestConfig(request).configure(table)
    return render(request,
                  'data_wrapper/resfinder_history.html',
                  {
                      'resfinderdata': resfinderdata,
                      'table': table,
                  })


@login_required
def generic_table(request, table_id, seqid_id):
    table_attributes = SavedTables.objects.get(pk=table_id).table_attributes
    seqid_list = SeqIdList.objects.get(pk=seqid_id).seqid_list
    table_data = get_table_data(table_attributes=table_attributes,
                                seqid_list=seqid_list)
    table_attributes.insert(0, 'SEQID')
    return render(request,
                  'data_wrapper/generic_table.html',
                  {
                      'table_attributes': table_attributes,
                      'table_data': table_data
                  })


@login_required
def query_results(request):
    return render(request,
                  'data_wrapper/query_results.html')


# This method and resfinderdata_table can probably be merged into one to make code less repeat-y. Look into this
@login_required
def seqdata_table(request):
    # Need to generate a column that will take user to an editing page.
    table = SeqDataTable(SeqData.objects.all(),
                         extra_columns=[('Edit', TemplateColumn('<a href="{% url \'data_wrapper:edit_data_seqdata\' seqdata_id=record.pk %}" class="btn btn-primary" role="button" aria-pressed="true">Edit Data</a>')),
                                        ('History', TemplateColumn('<a href="{% url \'data_wrapper:seqdata_history\' seqdata_id=record.pk %}" class="btn btn-outline-dark" role="button" aria-pressed="true">View History</a>'))])
    RequestConfig(request, paginate=False).configure(table)
    return render(request,
                  'data_wrapper/seqdata_table.html',
                  {
                      'table': table
                  })


@login_required
def resfinderdata_table(request):
    # Need to generate a column that will take user to an editing page.
    table = ResFinderDataTable(ResFinderData.objects.all(),
                               extra_columns=[('Edit', TemplateColumn('<a href="{% url \'data_wrapper:edit_data_resfinder\' resfinder_id=record.pk %}" class="btn btn-primary" role="button" aria-pressed="true">Edit Data</a>')),
                                              ('History', TemplateColumn('<a href="{% url \'data_wrapper:resfinder_history\' resfinder_id=record.pk %}" class="btn btn-outline-dark" role="button" aria-pressed="true">View History</a>'))])
    RequestConfig(request, paginate=False).configure(table)
    return render(request,
                  'data_wrapper/resfinderdata_table.html',
                  {
                       'table': table
                  }
                  )


@login_required
def edit_data_seqtracking(request, seqtracking_id):
    seqtracking = get_object_or_404(SeqTracking, pk=seqtracking_id)
    seqtracking_form = SeqTrackingEditForm(instance=seqtracking)
    if request.method == 'POST':
        seqtracking_form = SeqTrackingEditForm(request.POST)
        if seqtracking_form.is_valid():
            # Have to do some fancy footwork here to make the change reason save with the other form data.
            # Not entirely sure how this works, but it does, so I won't complain.
            s = SeqTrackingEditForm(request.POST, instance=seqtracking)
            change_reason = seqtracking_form.cleaned_data.get('change_reason')
            with_reason = s.save(commit=False)
            with_reason.changeReason = change_reason
            s.save()
            return redirect('data_wrapper:seqtracking_table')
    else:
        return render(request,
                      'data_wrapper/edit_data_seqtracking.html',
                      {'seqtracking_form': seqtracking_form},
                      )


@login_required
def create_data_seqtracking(request):
    seqtracking_form = SeqTrackingCreateForm()
    if request.method == 'POST':
        seqtracking_form = SeqTrackingCreateForm(request.POST)
        if seqtracking_form.is_valid():
            seqid = seqtracking_form.cleaned_data.get('seqid')
            lsts_id = seqtracking_form.cleaned_data.get('lsts_id')
            location = seqtracking_form.cleaned_data.get('location')
            oln_id = seqtracking_form.cleaned_data.get('oln_id')
            project = seqtracking_form.cleaned_data.get('project')
            priority = seqtracking_form.cleaned_data.get('priority')
            curator_flag = seqtracking_form.cleaned_data.get('curator_flag')
            comment = seqtracking_form.cleaned_data.get('comment')
            sample_exists = Sample.objects.filter(seqid=seqid).exists()
            lsts_exists = LSTSData.objects.filter(lsts_id=lsts_id).exists()
            if not sample_exists:
                Sample.objects.create(seqid=seqid)
            if not lsts_exists:
                LSTSData.objects.create(lsts_id=lsts_id,
                                        seqid=Sample.objects.get(seqid=seqid))
            try:
                SeqTracking.objects.update_or_create(seqid=Sample.objects.get(seqid=seqid),
                                                     lsts_id=LSTSData.objects.get(lsts_id=lsts_id),
                                                     location=location,
                                                     oln_id=oln_id,
                                                     project=project,
                                                     priority=priority,
                                                     curator_flag=curator_flag,
                                                     comment=comment)
            except:  # If SeqTracking object with specified SEQID or LSTS ID already exists, don't create.
                messages.error(request, 'ERROR: A SeqTracking entry already exists for either the SeqID or LSTS ID '
                                        'specified. Please verify what you have entered and try again.')
                pass
            return redirect('data_wrapper:seqtracking_table')
    return render(request,
                  'data_wrapper/create_data_seqtracking.html',
                  {
                      'seqtracking_form': seqtracking_form
                  })


@login_required
def seqtracking_history(request, seqtracking_id):
    seqtracking = get_object_or_404(SeqTracking, pk=seqtracking_id)
    histories = seqtracking.history.all()
    table = SeqTrackingTable(histories,
                             extra_columns=[('Date Changed', TemplateColumn('{{ record.history_date }}')),
                                            ('Changed By', TemplateColumn('{{ record.history_user }}')),
                                            ('Change Reason', TemplateColumn('{{ record.history_change_reason }}'))])
    RequestConfig(request).configure(table)
    return render(request,
                  'data_wrapper/seqtracking_history.html',
                  {
                      'seqtracking': seqtracking,
                      'table': table,
                  })


@login_required
def seqtracking_table(request):
    table = SeqTrackingTable(SeqTracking.objects.all(),
                             extra_columns=[('Edit', TemplateColumn('<a href="{% url \'data_wrapper:edit_data_seqtracking\' seqtracking_id=record.pk %}" class="btn btn-primary" role="button" aria-pressed="true">Edit Data</a>')),
                                            ('History', TemplateColumn('<a href="{% url \'data_wrapper:seqtracking_history\' seqtracking_id=record.pk %}" class="btn btn-outline-dark" role="button" aria-pressed="true">View History</a>'))])

    RequestConfig(request, paginate=False).configure(table)
    return render(request,
                  'data_wrapper/seqtracking_table.html',
                  {
                      'table': table
                  })


def get_table_data(table_attributes, seqid_list):
    table_data = list()
    models = [SeqData, LSTSData, ResFinderData, SeqTracking]
    for seqid in seqid_list:
        row_data = list()
        row_data.append(seqid)
        for attribute in table_attributes:
            for m in models:
                if attribute in get_model_fields(m):
                    model = m
                    field = m._meta.get_field(attribute)
            fieldname = str(field).split('.')[-1]
            data = model.objects.filter(seqid=Sample.objects.get(seqid=seqid))
            a = data.values_list(fieldname, flat=True)
            # It's possible that some stuff won't be in the database (for example, you can have SeqData uploaded but
            # no corresponding LSTS data) so, need to have this check to cover that case.
            if len(a) == 0:
                data_to_add = 'NA'
            # Most things should only have one entry - one n50, num_contigs per sample, etc.
            elif len(a) == 1:
                data_to_add = a[0]
            # Some things (i.e. resistance genes can have more than one entry per sample. Output those as a comma
            # separated string.
            else:
                data_to_add = ''
                for item in a:
                    data_to_add += item + ','
                data_to_add = data_to_add[:-1]
            row_data.append(data_to_add)
        table_data.append(row_data)
    return table_data


def decipher_input_request(attributes, operations, terms, combine_operations):
    # NOTE: This may not be a good way to do things at all, but as a proof of concept it seems to work.
    samples = Sample.objects.all()
    models = [Sample, SeqData, LSTSData, ResFinderData, SeqTracking]
    seqids = list()
    for i in range(len(attributes)):
        # Step 1: Find which model/field we're pulling stuff from.
        for m in models:
            if attributes[i] in get_model_fields(m):
                model = m
                field = model._meta.get_field(attributes[i])

        field_type = field.get_internal_type()
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
                return ['ERROR: When using a GREATER THAN or LESS THAN operation, you must enter a number.'
                        ' Please try again.']
            # Also make sure that field type is valid - can't call greater or less than on a charfield
            if field_type != 'IntegerField' and field_type != 'FloatField':
                return ['ERROR: Cannot use GREATER THAN operation on {fieldname}, as '
                        '{fieldname} is a {fieldtype}'.format(fieldname=fieldname,
                                                              fieldtype=field_type)]
            queryset = queryset.filter(**{fieldname + '__gt': term_as_integer})
        elif operations[i] == 'LESS THAN':
            try:
                term_as_integer = int(terms[i])
            except ValueError:
                return ['ERROR: When using a greater than or less than operation, you must enter a number.'
                        ' Please try again.']
            if field_type != 'IntegerField' and field_type != 'FloatField':
                return ['ERROR: Cannot use LESS THAN operation on {fieldname}, as '
                        '{fieldname} is a {fieldtype}'.format(fieldname=fieldname,
                                                              fieldtype=field_type)]
            queryset = queryset.filter(**{fieldname + '__lt': term_as_integer})
        elif operations[i] == 'BEFORE':
            if field_type != 'DateField':
                return ['ERROR: BEFORE and AFTER operations must be used on DateFields. {fieldname} is '
                        ' a {field_type}'.format(fieldname=fieldname,
                                                 field_type=field_type)]
            try:
                queryset = queryset.filter(**{fieldname + '__lt': terms[i]})
            except:
                return ['ERROR: Date format must be YYYY-MM-DD. Please re-enter your date in that format and try again.']
        elif operations[i] == 'AFTER':
            if field_type != 'DateField':
                return ['ERROR: BEFORE and AFTER operations must be used on DateFields. {fieldname} is '
                        ' a {field_type}'.format(fieldname=fieldname,
                                                 field_type=field_type)]
            try:
                queryset = queryset.filter(**{fieldname + '__gt': terms[i]})
            except:
                return ['ERROR: Date format must be YYYY-MM-DD. Please re-enter your date in that format and try again.']
        queryset_seqids = list()
        for item in queryset:
            queryset_seqids.append(str(item.seqid))

        # At this point we've filtered based on greaterthan/lessthan/contains for one query. Now need to decide what
        # to do based on whether an and or an or happened.
        # First thing - if this is our last operation, AND vs OR doesn't matter.
        if i == len(combine_operations) - 1:
            new_list = list()
            for sample in samples:
                if sample.seqid not in queryset_seqids:
                    samples = samples.exclude(seqid=sample.seqid)
            for sample in samples:
                new_list.append(sample.seqid)
            seqids.append(new_list)
        # Next case: AND - just keep going and filter queryset to be used in our next query down further.
        elif combine_operations[i] == 'AND':
            for sample in samples:
                if sample.seqid not in queryset_seqids:
                    samples = samples.exclude(seqid=sample.seqid)
        # Final case: OR - we'll need to generate a list of SEQIDs for this query and then refresh the sample set.
        elif combine_operations[i] == 'OR':
            new_list = list()
            for sample in samples:
                if sample.seqid not in queryset_seqids:
                    samples = samples.exclude(seqid=sample.seqid)
            for sample in samples:
                new_list.append(sample.seqid)
            seqids.append(new_list)
            samples = Sample.objects.all()

    query_result = list()
    for seqid_list in seqids:
        for seqid in seqid_list:
            if seqid not in query_result:
                query_result.append(seqid)
    return query_result


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

