from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
	url(r'^login$', auth_views.login, {'template_name': 'compta/connexion.html',}),
	url(r'^logout$', auth_views.logout, {'next_page': './login'}),


    url(r'^$', views.home),
    url(r'^article/(\d+)$', views.view_article),
]
