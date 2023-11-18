import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from config import settings
from config.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if DEBUG:
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
