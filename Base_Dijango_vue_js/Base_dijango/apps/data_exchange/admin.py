from django.contrib import admin

from .models import ImportJob, RowIssue

admin.site.register([ImportJob, RowIssue])
