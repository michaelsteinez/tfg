from django.contrib import admin
from django.urls import include, path
# from django.views.generic.base import TemplateView
from .views import HomeView

from modric import urls as modric_urls

urlpatterns = [
    path('modric/', include(modric_urls, namespace='modric')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path("", HomeView.as_view(), name="home"),
]
