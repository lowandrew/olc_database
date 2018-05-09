from django.contrib import admin
from .models import SeqData, LSTSData, ResFinderData, SavedQueries, SeqTracking, OLN, CultureData

# Register your models here.
admin.site.register(OLN)
admin.site.register(SeqData)
admin.site.register(LSTSData)
admin.site.register(ResFinderData)
admin.site.register(SavedQueries)
admin.site.register(SeqTracking)
admin.site.register(CultureData)
