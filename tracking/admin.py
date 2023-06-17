from django.contrib import admin
from tracking.models import Tracking

# Register your models here.


@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    # list_display = ('method', 'url', 'data')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
