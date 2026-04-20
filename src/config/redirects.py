from django.views.generic.base import RedirectView
from django.urls import path

redirects = [
    ('buy-1000.html', '/buy-1000/'),
    ('buy-2000.html', '/buy-2000/'),
]

urlpatterns = [
    path(old, RedirectView.as_view(url=new, permanent=True))
    for old, new in redirects
]
