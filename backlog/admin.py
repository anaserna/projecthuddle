from django.contrib import admin
from backlog.models import TrackHours
from backlog.models import TimeRecord

# Register your models here.
admin.site.register(TrackHours)
admin.site.register(TimeRecord)