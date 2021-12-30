from django.contrib import admin

from .forms import AnnouncementForm
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title','created_at','updated_at')
    form = AnnouncementForm

    def get_queryset(self, request):
        qs = super(AnnouncementAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()