# from django.conf import settings
# import debug_toolbar

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    # path('__debug__/', include(debug_toolbar.urls))
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
