import csv
from dal import autocomplete
from django_tables2 import RequestConfig
from django_tables2.columns import TemplateColumn
from django.shortcuts import render, get_object_or_404, redirect
from data_wrapper.models import LSTSData, SeqData, ResFinderData, SavedQueries, SavedTables, SeqIdList, SeqTracking, \
    OLN, CultureData, LstsIdList, OlnIdList
from .forms import SearchForm, BaseSearchFormSet, QuerySaveForm, ResFinderDataForm, SeqDataForm, CustomTableForm, \
    SeqTrackingCreateForm, SeqTrackingEditForm, CsvUploadForm
from .tables import SeqDataTable, ResFinderDataTable, SeqTrackingTable
from django.forms.formsets import formset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# make a list of models that we'll use in table building/query building
# IMPORTANT! The order of this must remain as is - LSTSData, OLN, and SeqData
# have to be first (AND IN THAT ORDER), as they're our 'primary(ish)' keys. Otherwise, querying will not work like
# it should
MODELS = [LSTSData, OLN, SeqData, ResFinderData, SeqTracking, CultureData]


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
            seqid_list = list(SeqData.objects.values_list('seqid', flat=True))
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
            seqids, olnids, lstsids = decipher_input_request(attributes, operations, terms, combine_operations)
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
                olnid_object = OlnIdList.objects.create(olnid_list=olnids)
                lstsid_object = LstsIdList.objects.create(lstsid_list=lstsids)
                return render(request,
                              'data_wrapper/query_results.html',
                              {
                                  'seqids': seqids,
                                  'olnids': olnids,
                                  'lstsids': lstsids,
                                  'saved_tables': saved_tables,
                                  'seqid_id': seqid_object.pk,
                                  'olnid_id': olnid_object.pk,
                                  'lstsid_id': lstsid_object.pk,
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
    if request.user != query.user:
        return render(request,
                      '403.html')
    return render(request,
                  'data_wrapper/delete_query_confirm.html',
                  {
                      'query': query
                  }
                  )


@login_required
def delete_table_confirm(request, table_id):
    table = get_object_or_404(SavedTables, pk=table_id)
    if request.user != table.user:
        return render(request,
                      '403.html')
    return render(request,
                  'data_wrapper/delete_table_confirm.html',
                  {
                      'table': table
                  }
                  )


@login_required
def delete_table(request, table_id):
    table = get_object_or_404(SavedTables, pk=table_id)
    if request.user != table.user:
        return render(request,
                      '403.html')
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
    else:
        return render(request,
                      'data_wrapper/edit_data_seqdata.html',
                      {'seqdata_form': seqdata_form},
                      )


@login_required
def delete_query(request, query_id):
    query = get_object_or_404(SavedQueries, pk=query_id)
    if request.user != query.user:
        return render(request,
                      '403.html')
    query.delete()
    return redirect('data_wrapper:saved_queries')


@login_required
def rerun_query(request, query_id):
    query = get_object_or_404(SavedQueries, pk=query_id)
    seqids, oln_ids, lsts_ids = decipher_input_request(attributes=query.search_attributes,
                                                       operations=query.search_operations,
                                                       terms=query.search_terms,
                                                       combine_operations=query.search_combine_operations)
    seqid_object = SeqIdList.objects.create(seqid_list=seqids)
    lstsid_object = LstsIdList.objects.create(lstsid_list=lsts_ids)
    olnid_object = OlnIdList.objects.create(olnid_list=oln_ids)
    saved_tables = SavedTables.objects.filter(user=request.user)
    return render(request,
                  'data_wrapper/query_results.html',
                  {
                      'seqids': seqids,
                      'lstsids': lsts_ids,
                      'olnids': oln_ids,
                      'saved_tables': saved_tables,
                      'seqid_id': seqid_object.pk,
                      'olnid_id': olnid_object.pk,
                      'lstsid_id': lstsid_object.pk
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
def generic_table(request, table_id, seqid_id, olnid_id, lstsid_id):
    table_attributes = SavedTables.objects.get(pk=table_id).table_attributes
    seqid_list = SeqIdList.objects.get(pk=seqid_id).seqid_list
    olnid_list = OlnIdList.objects.get(pk=olnid_id).olnid_list
    lstsid_list = LstsIdList.objects.get(pk=lstsid_id).lstsid_list
    table_data = get_table_data(table_attributes=table_attributes,
                                seqid_list=seqid_list)
    table_attributes.insert(0, 'SEQID')
    # Need to also have OLN-based and LSTS-based data added here - will be somewhat tricky.
    oln_table_attributes = SavedTables.objects.get(pk=table_id).table_attributes
    oln_table_data = get_table_data_oln(oln_table_attributes,
                                        olnid_list=olnid_list)
    oln_table_attributes.insert(0, 'OLNID')
    # LSTS
    lsts_table_attributes = SavedTables.objects.get(pk=table_id).table_attributes
    lsts_table_data = get_table_data_lsts(lsts_table_attributes,
                                          lstsid_list=lstsid_list)
    lsts_table_attributes.insert(0, 'LSTSID')
    return render(request,
                  'data_wrapper/generic_table.html',
                  {
                      'table_attributes': table_attributes,
                      'table_data': table_data,
                      'oln_table_attributes': oln_table_attributes,
                      'oln_table_data': oln_table_data,
                      'lsts_table_attributes': lsts_table_attributes,
                      'lsts_table_data': lsts_table_data
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
            oln_id = seqtracking_form.cleaned_data.get('oln_id')
            priority = seqtracking_form.cleaned_data.get('priority')
            curator_flag = seqtracking_form.cleaned_data.get('curator_flag')
            comment = seqtracking_form.cleaned_data.get('comment')
            seqid_exists = SeqData.objects.filter(seqid=seqid).exists()
            olnid_exists = OLN.objects.filter(oln_id=oln_id).exists()
            lstsid_exists = LSTSData.objects.filter(lsts_id=lsts_id).exists()
            # Create our objects if they don't already exist.
            if not seqid_exists:
                SeqData.objects.create(seqid=seqid)
            if not olnid_exists:
                OLN.objects.create(oln_id=oln_id)
            if not lstsid_exists:
                LSTSData.objects.create(lsts_id=lsts_id)

            # Also update the SeqData to point back to the LSTS/OLN data
            SeqData.objects.filter(seqid=seqid).update(oln_id=OLN.objects.get(oln_id=oln_id),
                                                       lsts_id=LSTSData.objects.get(lsts_id=lsts_id))
            try:
                SeqTracking.objects.update_or_create(seqid=SeqData.objects.get(seqid=seqid),
                                                     lsts_id=LSTSData.objects.get(lsts_id=lsts_id),
                                                     oln_id=OLN.objects.get(oln_id=oln_id),
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


@login_required
def upload_seqtracking_csv(request):
    form = CsvUploadForm()
    if request.method == 'POST':
        form = CsvUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Turns out we get excel files for this, not CSV. Will need to use pandas read_excel.
            csv_file = request.FILES['csv_file']
            reader = csv.DictReader(csv_file.read().decode('utf-8'))
            for row in reader:
                print(row)
            messages.success(request, 'File was uploaded! :D')
            return redirect('data_wrapper:seqtracking_table')
        return render(request,
                      'data_wrapper/upload_seqtracking_csv.html',
                      {
                          'form': form
                      })
    else:
        return render(request,
                      'data_wrapper/upload_seqtracking_csv.html',
                      {
                          'form': form
                      })


def get_table_data(table_attributes, seqid_list):
    # Need to figure out the best approach to this: Given a list of SEQIDs, will need to know which
    # OLN and LSTS IDs they're linked to so that we can also retrieve OLN and LSTS-related data for the query.
    table_data = list()
    for seqid in seqid_list:
        seqdata = SeqData.objects.get(seqid=seqid)
        oln_id = str(seqdata.oln_id)
        lsts_id = str(seqdata.lsts_id)
        row_data = list()
        row_data.append(seqid)
        for attribute in table_attributes:
            for m in MODELS:
                if attribute in get_model_fields(m):
                    model = m
                    field = m._meta.get_field(attribute)
                    break
            fieldname = str(field).split('.')[-1]
            # This try/except is super ugly, but seems to work.
            try:
                data = model.objects.filter(seqid=SeqData.objects.get(seqid=seqid))
                a = data.values_list(fieldname, flat=True)
            except:
                try:
                    data = model.objects.filter(oln_id=OLN.objects.get(oln_id=oln_id))
                    a = data.values_list(fieldname, flat=True)
                except:
                    try:
                        data = model.objects.filter(lsts_id=LSTSData.objects.get(lsts_id=lsts_id))
                        a = data.values_list(fieldname, flat=True)
                    except:
                        a = list()
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
                    data_to_add += str(item) + ','
                data_to_add = data_to_add[:-1]
            row_data.append(data_to_add)
        table_data.append(row_data)
    return table_data


# I'm pretty sure this is just different enough from the SEQID case that rewriting that method
# to be able to handle OLN input is more work that just making this. In any case, this is also not very
# DRY and should be looked at not too far in the future.
def get_table_data_oln(table_attributes, olnid_list):
    table_data = list()
    for oln_id in olnid_list:
        olndata = OLN.objects.get(oln_id=oln_id)
        # Get all SEQIDs associate with olndata.
        seqdata_objects = SeqData.objects.filter(oln_id=olndata)
        # Also get lsts data associated with OLN, if it exists. Made possible with __str__ methods in models.py
        lsts_data = str(olndata.lsts_id)
        # Setup our row.
        row_data = list()
        row_data.append(oln_id)
        # Now iterate through our attributes.
        for attribute in table_attributes:
            for m in MODELS:
                if attribute in get_model_fields(m):
                    model = m
                    field = m._meta.get_field(attribute)
                    break
            fieldname = str(field).split('.')[-1]
            # Now that we've done that, try to extract information using an ugly try/except.
            try:
                data = model.objects.filter(oln_id=OLN.objects.get(oln_id=oln_id))
                a = data.values_list(fieldname, flat=True)
            except:
                try:
                    data = model.objects.filter(lsts_id=LSTSData.objects.get(lsts_id=lsts_data))
                    a = data.values_list(fieldname, flat=True)
                except:
                    try:
                        a = list()
                        for seqdata in seqdata_objects:
                            data = model.objects.filter(seqid=SeqData.objects.get(seqid=seqdata.seqid))
                            temp_data = data.values_list(fieldname, flat=True)
                            a.append(temp_data)
                    except:
                        a = list()

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
                    data_to_add += str(item) + ','
                data_to_add = data_to_add[:-1]
            row_data.append(data_to_add)
        table_data.append(row_data)
    return table_data


def get_table_data_lsts(table_attributes, lstsid_list):
    table_data = list()
    for lsts_id in lstsid_list:
        lstsdata = LSTSData.objects.get(lsts_id=lsts_id)
        # Get all SEQIDs and OLNIDs associated with LSTS.
        seqdata_objects = SeqData.objects.filter(lsts_id=lstsdata)
        olndata_objects = OLN.objects.filter(lsts_id=lstsdata)
        # Setup our row.
        row_data = list()
        row_data.append(lsts_id)
        # Now iterate through our attributes.
        for attribute in table_attributes:
            for m in MODELS:
                if attribute in get_model_fields(m):
                    model = m
                    field = m._meta.get_field(attribute)
                    break
            fieldname = str(field).split('.')[-1]
            # Now that we've done that, try to extract information using an ugly try/except.
            try:
                data = model.objects.filter(lsts_id=LSTSData.objects.get(lsts_id=lstsdata))
                a = data.values_list(fieldname, flat=True)
            except:
                try:
                    a = list()
                    for olndata in olndata_objects:
                        data = model.objects.filter(oln_id=OLN.objects.get(oln_id=olndata.oln_id))
                        temp_data = data.values_list(fieldname, flat=True)
                        a.append(temp_data)
                except:
                    try:
                        a = list()
                        for seqdata in seqdata_objects:
                            data = model.objects.filter(seqid=SeqData.objects.get(seqid=seqdata.seqid))
                            temp_data = data.values_list(fieldname, flat=True)
                            a.append(temp_data)
                    except:
                        a = list()

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
                    data_to_add += str(item) + ','
                data_to_add = data_to_add[:-1]
            row_data.append(data_to_add)
        table_data.append(row_data)
    return table_data


def decipher_input_request(attributes, operations, terms, combine_operations):
    # NOTE: This may not be a good way to do things at all, but as a proof of concept it seems to work.
    # I think the I need to keep track of LSTS, OLN, and SeqID, and then have results for each.
    # Will probably display these results in different tabs. This may or may not be not at all how to proceed.
    # Will need to do wome more thinking.
    seqids = list()
    olnids = list()
    lstsids = list()
    for i in range(len(attributes)):
        # Step 1: Find which model/field we're pulling stuff from.
        for m in MODELS:
            if attributes[i] in get_model_fields(m):
                model = m
                field = model._meta.get_field(attributes[i])
                break

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
                # This function always needs to return three things - this seems really clumsy.
                return ['ERROR: When using a GREATER THAN or LESS THAN operation, you must enter a number.'
                        ' Please try again.'], [], []
            # Also make sure that field type is valid - can't call greater or less than on a charfield
            if field_type != 'IntegerField' and field_type != 'FloatField':
                return ['ERROR: Cannot use GREATER THAN operation on {fieldname}, as '
                        '{fieldname} is a {fieldtype}'.format(fieldname=fieldname,
                                                              fieldtype=field_type)], [], []
            queryset = queryset.filter(**{fieldname + '__gt': term_as_integer})
        elif operations[i] == 'LESS THAN':
            try:
                term_as_integer = int(terms[i])
            except ValueError:
                return ['ERROR: When using a greater than or less than operation, you must enter a number.'
                        ' Please try again.'], [], []
            if field_type != 'IntegerField' and field_type != 'FloatField':
                return ['ERROR: Cannot use LESS THAN operation on {fieldname}, as '
                        '{fieldname} is a {fieldtype}'.format(fieldname=fieldname,
                                                              fieldtype=field_type)], [], []
            queryset = queryset.filter(**{fieldname + '__lt': term_as_integer})
        elif operations[i] == 'BEFORE':
            if field_type != 'DateField':
                return ['ERROR: BEFORE and AFTER operations must be used on DateFields. {fieldname} is '
                        ' a {field_type}'.format(fieldname=fieldname,
                                                 field_type=field_type)], [], []
            try:
                queryset = queryset.filter(**{fieldname + '__lt': terms[i]})
            except:
                return ['ERROR: Date format must be YYYY-MM-DD. Please re-enter your date in that format and try again.'], [], []
        elif operations[i] == 'AFTER':
            if field_type != 'DateField':
                return ['ERROR: BEFORE and AFTER operations must be used on DateFields. {fieldname} is '
                        ' a {field_type}'.format(fieldname=fieldname,
                                                 field_type=field_type)], [], []
            try:
                queryset = queryset.filter(**{fieldname + '__gt': terms[i]})
            except:
                return ['ERROR: Date format must be YYYY-MM-DD. Please re-enter your date in that format and try again.'], [], []

        queryset_seqids = list()
        queryset_olnids = list()
        queryset_lstsids = list()

        # First loop through queryset will be for seqids.
        # TODO: only get model fields once per loop - current implementation is resource wasting
        for item in queryset:
            if 'seqid' in get_model_fields(item):
                # This only works because I have __str__ methods defined. Make sure new models have them.
                queryset_seqids.append(str(item))
            elif 'oln_id' in get_model_fields(item):
                # Can possibly have more than one SEQID associated with an OLN ID. Use filter to get
                # any/all SEQIDs associated with the oln_id
                seqdata_objects = SeqData.objects.filter(oln_id__oln_id__exact=str(item))
                for seqdata in seqdata_objects:
                    queryset_seqids.append(str(seqdata))
            elif 'lsts_id' in get_model_fields(item):
                # This is essentially the exact same as OLN ID - can have more than one SEQID per LSTS, so
                # get a list of any/all SEQIDs associated with LSTS ID
                seqdata_objects = SeqData.objects.filter(lsts_id__lsts_id__exact=str(item))
                for seqdata in seqdata_objects:
                    queryset_seqids.append(str(seqdata))

        # Now attempt to take care of OLN IDs.
        for item in queryset:
            if 'oln_id' in get_model_fields(item) and 'seqid' not in get_model_fields(item):
                # This takes care of everything but accessory sequence data (resfinder, confindr, etc) and LSTS.
                queryset_olnids.append(str(item))
            elif 'seqid' in get_model_fields(item):
                # First, get the SeqData object, as this deals with accessory sequence data.
                # Then, need to get the OLN ID associated with the SeqData, if it exists.
                seqdata = SeqData.objects.get(seqid=item.seqid)
                if str(seqdata.oln_id) != 'None':  # Don't let null values get through
                    queryset_olnids.append(str(seqdata.oln_id))
            elif 'lsts_id' in get_model_fields(item):
                # This should only ever be for the LSTSData object - all others are covered under olnid or seqid
                oln_objects = OLN.objects.filter(lsts_id__lsts_id__exact=str(item))
                for oln_data in oln_objects:
                    queryset_olnids.append(str(oln_data))

        # Finally, take care of LSTS IDs
        for item in queryset:
            if 'lsts_id' in get_model_fields(item) and 'seqid' not in get_model_fields(item) and 'oln_id' not in get_model_fields(item):
                # This takes care of only the LSTSData itself.
                queryset_lstsids.append(str(item))
            elif 'oln_id' in get_model_fields(item) and 'lsts_id' in get_model_fields(item) and 'seqid' not in get_model_fields(item):
                # Next need to take care of things that have OLN ID and LSTSID but no SEQID - this covers OLN
                queryset_lstsids.append(str(item.lsts_id))
            elif 'seqid' in get_model_fields(item) and 'lsts_id' in get_model_fields(item):
                # This should covers seqdata, which should give us LSTS ID easily
                queryset_lstsids.append(str(item.lsts_id))
            elif 'seqid' in get_model_fields(item) and 'lsts_id' not in get_model_fields(item):
                seqdata = SeqData.objects.get(seqid=str(item))
                queryset_lstsids.append(str(seqdata.lsts_id))
            elif 'oln_id' in get_model_fields(item):
                # Now need to cover CultureData.
                oln_objects = OLN.objects.filter(oln_id=str(item))
                for oln_object in oln_objects:
                    queryset_lstsids.append(str(oln_object.lsts_id))

        # At this point we've filtered based on greaterthan/lessthan/contains for one query. Now need to decide what
        # to do based on whether an and or an or happened.
        # First thing - if this is our last operation, AND vs OR doesn't matter.
        samples = SeqData.objects.all()
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
            samples = SeqData.objects.all()

        # Now do the exact thing that we did for SEQID for OLNID.
        # TODO: Write a separate function once I know this works, because this is not DRY.
        oln_samples = OLN.objects.all()
        if i == len(combine_operations) - 1:
            new_list = list()
            for sample in oln_samples:
                if sample.oln_id not in queryset_olnids:
                    oln_samples = oln_samples.exclude(oln_id=sample.oln_id)
            for sample in oln_samples:
                new_list.append(sample.oln_id)
            olnids.append(new_list)
        # Next case: AND - just keep going and filter queryset to be used in our next query down further.
        elif combine_operations[i] == 'AND':
            for sample in oln_samples:
                if sample.oln_id not in queryset_olnids:
                    oln_samples = oln_samples.exclude(oln_id=sample.oln_id)
        # Final case: OR - we'll need to generate a list of SEQIDs for this query and then refresh the sample set.
        elif combine_operations[i] == 'OR':
            new_list = list()
            for sample in oln_samples:
                if sample.oln_id not in queryset_olnids:
                    oln_samples = oln_samples.exclude(oln_id=sample.oln_id)
            for sample in samples:
                new_list.append(sample.oln_id)
            olnids.append(new_list)
            oln_samples = OLN.objects.all()

        # Finally (again) get LSTS ID out.
        lsts_samples = LSTSData.objects.all()
        if i == len(combine_operations) - 1:
            new_list = list()
            for sample in lsts_samples:
                if sample.lsts_id not in queryset_lstsids:
                    lsts_samples = lsts_samples.exclude(lsts_id=sample.lsts_id)
            for sample in lsts_samples:
                new_list.append(sample.lsts_id)
            lstsids.append(new_list)
        # Next case: AND - just keep going and filter queryset to be used in our next query down further.
        elif combine_operations[i] == 'AND':
            for sample in lsts_samples:
                if sample.lsts_id not in queryset_lstsids:
                    lsts_samples = lsts_samples.exclude(lsts_id=sample.lsts_id)
        # Final case: OR - we'll need to generate a list of SEQIDs for this query and then refresh the sample set.
        elif combine_operations[i] == 'OR':
            new_list = list()
            for sample in lsts_samples:
                if sample.lsts_id not in queryset_lstsids:
                    lsts_samples = lsts_samples.exclude(lsts_id=sample.lsts_id)
            for sample in samples:
                new_list.append(sample.lsts_id)
            lstsids.append(new_list)
            lsts_samples = LSTSData.objects.all()

    seqid_result = list()
    for seqid_list in seqids:
        for seqid in seqid_list:
            if seqid not in seqid_result:
                seqid_result.append(seqid)

    olnid_result = list()
    for olnid_list in olnids:
        for olnid in olnid_list:
            if olnid not in olnid_result:
                olnid_result.append(olnid)

    lstsid_result = list()
    for lstsid_list in lstsids:
        for lstsid in lstsid_list:
            if lstsid not in lstsid_result:
                lstsid_result.append(lstsid)
    return seqid_result, olnid_result, lstsid_result


def get_model_fields(model):
    fields = list()
    for field in model._meta.fields:
        field_id = str(field).split('.')[-1]
        fields.append(field_id)
    return fields


def make_list_of_fields():
    fields = list()  # Would use a set here, but django-autocomplete-light wants a list.
    for model in MODELS:
        for field in get_model_fields(model):
            if field not in fields:
                fields.append(field)
    return fields

