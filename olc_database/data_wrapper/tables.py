import django_tables2 as tables
from data_wrapper.models import SeqData, ResFinderData, SeqTracking, OLN, CultureData


class SeqDataTable(tables.Table):
    class Meta:
        model = SeqData
        attrs = {'id': 'seqdata-table',
                 'class': 'table table-hover compact'}


class ResFinderDataTable(tables.Table):
    class Meta:
        model = ResFinderData
        attrs = {'id': 'resfinderdata-table',
                 'class': 'table table-hover compact'}


class SeqTrackingTable(tables.Table):
    class Meta:
        model = SeqTracking
        attrs = {'id': 'seqtracking-table',
                 'class': 'table table-hover compact'}


class OLNTable(tables.Table):
    class Meta:
        model = OLN
        attrs = {'id': 'oln-table',
                 'class': 'table table-hover compact'}


class CultureDataTable(tables.Table):
    class Meta:
        model = CultureData
        attrs = {'id': 'culturedata-table',
                 'class': 'table table-hover compact'}
