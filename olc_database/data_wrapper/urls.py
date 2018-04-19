from django.conf.urls import url

from olc_database.data_wrapper.views import AttributeAutocompleteFromList
from olc_database.data_wrapper import views

app_name = 'data_wrapper'
urlpatterns = [
    url(r'^query_builder$', views.query_builder, name='query_builder'),
    url(r'^attribute-autocomplete/$',
        AttributeAutocompleteFromList.as_view(),
        name='attribute-autocomplete'),
]
