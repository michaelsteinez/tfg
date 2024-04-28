from django.contrib import admin
from django.urls import include, path

from modric import urls as modric_urls

urlpatterns = [
    path('modric/', include(modric_urls, namespace='modric')),
    path('admin/', admin.site.urls),
]
