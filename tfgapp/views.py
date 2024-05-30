from django.shortcuts import redirect
from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('modric:index')
        return super().dispatch(request, *args, **kwargs)
