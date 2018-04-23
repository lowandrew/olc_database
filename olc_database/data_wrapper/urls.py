from django.conf.urls import url

from olc_database.data_wrapper.views import AttributeAutocompleteFromList
from olc_database.data_wrapper import views

app_name = 'data_wrapper'
urlpatterns = [
    url(r'^query_builder$', views.query_builder, name='query_builder'),
    url(r'^query_results$', views.query_results, name='query_results'),
    url(r'^seqdata_table$', views.seqdata_table, name='seqdata_table'),
    url(r'^resfinderdata_table$', views.resfinderdata_table, name='resfinderdata_table'),
    url(r'^saved_queries$', views.saved_queries, name='saved_queries'),
    url(r'^delete_query_confirm/(?P<query_id>\d+)/$', views.delete_query_confirm, name='delete_query_confirm'),
    url(r'^delete_query/(?P<query_id>\d+)/$', views.delete_query, name='delete_query'),
    url(r'^rerun_query/(?P<query_id>\d+)/$', views.rerun_query, name='rerun_query'),
    url(r'^query_details/(?P<query_id>\d+)/$', views.query_details, name='query_details'),
    url(r'^edit_data_resfinder/(?P<resfinder_id>\d+)/$', views.edit_data_resfinder, name='edit_data_resfinder'),
    url(r'^edit_data_seqdata/(?P<seqdata_id>\d+)/$', views.edit_data_seqdata, name='edit_data_seqdata'),
    url(r'^attribute-autocomplete/$',
        AttributeAutocompleteFromList.as_view(),
        name='attribute-autocomplete'),
]
