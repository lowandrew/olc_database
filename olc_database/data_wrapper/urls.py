from django.conf.urls import url

from olc_database.data_wrapper.views import AttributeAutocompleteFromList
from olc_database.data_wrapper import views

app_name = 'data_wrapper'
urlpatterns = [
    url(r'^query_builder$', views.query_builder, name='query_builder'),
    url(r'^query_results$', views.query_results, name='query_results'),
    url(r'^seqdata_table$', views.seqdata_table, name='seqdata_table'),
    url(r'^attribute-autocomplete/$',
        AttributeAutocompleteFromList.as_view(),
        name='attribute-autocomplete'),
]
