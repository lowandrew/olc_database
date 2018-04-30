from django.conf.urls import url

from olc_database.data_wrapper.views import AttributeAutocompleteFromList
from olc_database.data_wrapper import views

# TODO: Reorder urlpatterns to have more logical structure/space them out and comment them better

app_name = 'data_wrapper'
urlpatterns = [
    url(r'^query_builder$', views.query_builder, name='query_builder'),
    url(r'^upload_seqtracking_csv$', views.upload_seqtracking_csv, name='upload_seqtracking_csv'),
    url(r'^create_data_seqtracking$', views.create_data_seqtracking, name='create_data_seqtracking'),
    url(r'^generic_table/table-(?P<table_id>\d+)/seqid-(?P<seqid_id>\d+)/$', views.generic_table, name='generic_table'),
    url(r'^table_builder$', views.table_builder, name='table_builder'),
    url(r'^query_results$', views.query_results, name='query_results'),
    url(r'^seqdata_table$', views.seqdata_table, name='seqdata_table'),
    url(r'^seqtracking_table$', views.seqtracking_table, name='seqtracking_table'),
    url(r'^resfinderdata_table$', views.resfinderdata_table, name='resfinderdata_table'),
    url(r'^saved_queries$', views.saved_queries, name='saved_queries'),
    url(r'^delete_query_confirm/(?P<query_id>\d+)/$', views.delete_query_confirm, name='delete_query_confirm'),
    url(r'^delete_table_confirm/(?P<table_id>\d+)/$', views.delete_table_confirm, name='delete_table_confirm'),
    url(r'^delete_query/(?P<query_id>\d+)/$', views.delete_query, name='delete_query'),
    url(r'^delete_table/(?P<table_id>\d+)/$', views.delete_table, name='delete_table'),
    url(r'^rerun_query/(?P<query_id>\d+)/$', views.rerun_query, name='rerun_query'),
    url(r'^query_details/(?P<query_id>\d+)/$', views.query_details, name='query_details'),
    url(r'^edit_data_resfinder/(?P<resfinder_id>\d+)/$', views.edit_data_resfinder, name='edit_data_resfinder'),
    url(r'^edit_data_seqtracking/(?P<seqtracking_id>\d+)/$', views.edit_data_seqtracking, name='edit_data_seqtracking'),
    url(r'^edit_data_seqdata/(?P<seqdata_id>\d+)/$', views.edit_data_seqdata, name='edit_data_seqdata'),
    url(r'^seqtracking_history/(?P<seqtracking_id>\d+)/$', views.seqtracking_history, name='seqtracking_history'),
    url(r'^seqdata_history/(?P<seqdata_id>\d+)/$', views.seqdata_history, name='seqdata_history'),
    url(r'^resfinder_history/(?P<resfinder_id>\d+)/$', views.resfinder_history, name='resfinder_history'),
    url(r'^attribute-autocomplete/$',
        AttributeAutocompleteFromList.as_view(),
        name='attribute-autocomplete'),
]
