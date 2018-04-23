from django.contrib import admin
from .models import Sample, SeqData, LSTSData, ResFinderData, SavedQueries

# Register your models here.
admin.site.register(Sample)
admin.site.register(SeqData)
admin.site.register(LSTSData)
admin.site.register(ResFinderData)
admin.site.register(SavedQueries)
