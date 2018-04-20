import django_tables2 as tables
from data_wrapper.models import SeqData


class SeqDataTable(tables.Table):
    class Meta:
        model = SeqData
        attrs = {'id': 'seqdata-table',
                 'class': 'table table-hover table-border'}
