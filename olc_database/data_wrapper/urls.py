from django.conf.urls import url

from olc_database.data_wrapper import views

app_name = 'data_wrapper'
urlpatterns = [
    url(r'^query_builder$', views.query_builder, name='query_builder')
]
