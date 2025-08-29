from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from chat_app import urls as chat_app_urls

admin.site.site_header = 'Meng Meng'
admin.site.index_title = 'Meng'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('root_directory/api/', include('chat_app.urls')),
]

if settings.DEBUG:
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    




