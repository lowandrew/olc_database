from django.contrib import admin
from .models import Sample, SeqData, LSTSData, ResFinderData, SavedQueries, SeqTracking

# Register your models here.
admin.site.register(Sample)
admin.site.register(SeqData)
admin.site.register(LSTSData)
admin.site.register(ResFinderData)
admin.site.register(SavedQueries)
admin.site.register(SeqTracking)
