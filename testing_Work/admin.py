from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TestingJob

class TestingJobAdmin(admin.ModelAdmin):

    list_display = (
        'SRF',
        'job_no',
        'assigned_to',
        'status',
        'amount',
        'received_date'
    )

    list_filter = ('status','assigned_to')

    search_fields = ('job_no','SRF')

admin.site.register(TestingJob, TestingJobAdmin)
