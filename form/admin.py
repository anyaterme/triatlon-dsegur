from django.contrib import admin

# Register your models here.
from .models import IncidentForm
@admin.register(IncidentForm)
class IncidentFormAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'incident_date', 'talon_required', 'parte_required', 'date_submitted', 'uuid')
    search_fields = ('first_name', 'last_name', 'email', 'location')
    list_filter = ('talon_required', 'parte_required', 'incident_date', 'date_submitted')
    ordering = ('-date_submitted',)
    readonly_fields = ('uuid', 'date_submitted')

    class Meta:
        model = IncidentForm
admin.site.site_header = "Darsim Incident Form Admin"
admin.site.site_title = "Darsim Incident Form Admin Portal"
admin.site.index_title = "Welcome to Darsim Incident Form Admin Portal"

