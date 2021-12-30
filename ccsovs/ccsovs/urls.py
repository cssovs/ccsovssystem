from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from settings.views import upload_bulk

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', include('public.urls')),
    path('upload/', upload_bulk, name='upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Online Voting System"
admin.site.index_title = "Welcome to online voting system admin panel"
admin.site.site_title = "OVS"
