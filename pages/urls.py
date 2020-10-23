from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.index, name='index'),
    url(r'^contact-us/$', views.contact, name='contact-us'),
    url(r'^about-us/$', views.about, name='about-us'),
    url(r'^panel/$', views.panel, name='panel'),
    # start of site pages

]
