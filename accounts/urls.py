from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
	url(r'^login$', auth_views.login, {'template_name': 'accounts/login.html',}),
	url(r'^logout$', auth_views.logout, {'next_page': '/'}),
	url(r'^create$', views.create_account),
	url(r'^redirect$', views.account_created),

]
