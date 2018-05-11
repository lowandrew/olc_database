import django_tables2 as tables
from data_wrapper.models import SeqData, ResFinderData, SeqTracking, OLN


class SeqDataTable(tables.Table):
    class Meta:
        model = SeqData
        attrs = {'id': 'seqdata-table',
                 'class': 'table table-hover table-border compact table-sm table-responsive'}


class ResFinderDataTable(tables.Table):
    class Meta:
        model = ResFinderData
        attrs = {'id': 'resfinderdata-table',
                 'class': 'table table-hover table-border compact'}


class SeqTrackingTable(tables.Table):
    class Meta:
        model = SeqTracking
        attrs = {'id': 'seqtracking-table',
                 'class': 'table table-hover table-border compact'}


class OLNTable(tables.Table):
    class Meta:
        model = OLN
        attrs = {'id': 'oln-table',
                 'class': 'table table-hover table-border compact'}
