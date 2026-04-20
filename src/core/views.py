from django.views.generic import TemplateView
from django.shortcuts import render


def page_not_found(request, exception):
    return render(request, 'errors/404.html', status=404)

def permission_denied(request, exception):
    return render(request, 'errors/403.html', status=403)

def bad_request(request, exception):
    return render(request, 'errors/400.html', status=400)

def server_error(request):
    return render(request, 'errors/500.html', status=500)


class HomePageView(TemplateView):
    template_name = 'welcome.html'

