from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import include, path

from .views import HomeView

from modric import urls as modric_urls

urlpatterns = [
    path('modric/', include(modric_urls, namespace='modric')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", HomeView.as_view(), name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
