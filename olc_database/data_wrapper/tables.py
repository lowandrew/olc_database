import django_tables2 as tables
from data_wrapper.models import SeqData, ResFinderData


class SeqDataTable(tables.Table):
    class Meta:
        model = SeqData
        attrs = {'id': 'seqdata-table',
                 'class': 'table table-hover table-border'}


class ResFinderDataTable(tables.Table):
    class Meta:
        model = ResFinderData
        attrs = {'id': 'resfinderdata-table',
                 'class': 'table table-hover table-border'}
