from django.conf.urls import url

from olc_database.data_wrapper.views import AttributeAutocompleteFromList
from olc_database.data_wrapper import views


app_name = 'data_wrapper'
urlpatterns = [
    # Query-related things: query builder, query results, query details, rerunning of queries
    url(r'^query_builder$', views.query_builder, name='query_builder'),
    url(r'^query_results$', views.query_results, name='query_results'),
    url(r'^rerun_query/(?P<query_id>\d+)/$', views.rerun_query, name='rerun_query'),
    url(r'^query_details/(?P<query_id>\d+)/$', views.query_details, name='query_details'),

    # Custom table related things: table builder and generic table viewer.
    url(r'^table_builder$', views.table_builder, name='table_builder'),
    url(r'^generic_table/table-(?P<table_id>\d+)/seqid-(?P<seqid_id>\d+)/olnid-(?P<olnid_id>\d+)/lstsid-(?P<lstsid_id>\d+)/$', views.generic_table, name='generic_table'),

    # Data table viewing - SeqData, ResFinder, OLN, LSTS, etc.
    url(r'^seqdata_table$', views.seqdata_table, name='seqdata_table'),
    url(r'^oln_table$', views.oln_table, name='oln_table'),
    url(r'^seqtracking_table$', views.seqtracking_table, name='seqtracking_table'),
    url(r'^resfinderdata_table$', views.resfinderdata_table, name='resfinderdata_table'),
    url(r'^culturedata_table$', views.culturedata_table, name='culturedata_table'),

    # Data table editing - SeqData, ResFinder, OLN, LSTS, etc.
    url(r'^edit_data_resfinder/(?P<resfinder_id>\d+)/$', views.edit_data_resfinder, name='edit_data_resfinder'),
    url(r'^edit_data_oln/(?P<oln_id>\d+)/$', views.edit_data_oln, name='edit_data_oln'),
    url(r'^edit_data_seqtracking/(?P<seqtracking_id>\d+)/$', views.edit_data_seqtracking, name='edit_data_seqtracking'),
    url(r'^edit_data_seqdata/(?P<seqdata_id>\d+)/$', views.edit_data_seqdata, name='edit_data_seqdata'),
    url(r'^edit_data_culturedata/(?P<culturedata_id>\d+)/$', views.edit_data_culturedata, name='edit_data_culturedata'),


    # Data  table histories - for all the usual suspects.
    url(r'^seqtracking_history/(?P<seqtracking_id>\d+)/$', views.seqtracking_history, name='seqtracking_history'),
    url(r'^seqdata_history/(?P<seqdata_id>\d+)/$', views.seqdata_history, name='seqdata_history'),
    url(r'^resfinder_history/(?P<resfinder_id>\d+)/$', views.resfinder_history, name='resfinder_history'),
    url(r'^oln_history/(?P<oln_id>\d+)/$', views.oln_history, name='oln_history'),
    url(r'^culturedata_history/(?P<culturedata_id>\d+)/$', views.culturedata_history, name='culturedata_history'),

    # Data creation - SeqTracking, OLN, and more!
    url(r'^create_data_seqtracking$', views.create_data_seqtracking, name='create_data_seqtracking'),
    url(r'^create_data_oln$', views.create_data_oln, name='create_data_oln'),
    url(r'^create_data_lsts$', views.create_data_lsts, name='create_data_lsts'),
    url(r'^create_data_culturedata$', views.create_data_culturedata, name='create_data_culturedata'),

    # Saved queries
    url(r'^saved_queries$', views.saved_queries, name='saved_queries'),

    # Table and query deletion and deletion confirmations
    url(r'^delete_query_confirm/(?P<query_id>\d+)/$', views.delete_query_confirm, name='delete_query_confirm'),
    url(r'^delete_table_confirm/(?P<table_id>\d+)/$', views.delete_table_confirm, name='delete_table_confirm'),
    url(r'^delete_query/(?P<query_id>\d+)/$', views.delete_query, name='delete_query'),
    url(r'^delete_table/(?P<table_id>\d+)/$', views.delete_table, name='delete_table'),

    # Attribute autocomplete view needed by django-autocomplete-light
    url(r'^attribute-autocomplete/$',
        AttributeAutocompleteFromList.as_view(),
        name='attribute-autocomplete'),
]
