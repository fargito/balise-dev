from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
	url(r'^login$', auth_views.login, {'template_name': 'accounts/login.html',}),
	url(r'^logout$', auth_views.logout, {'next_page': '/'}),
	url(r'^password_change$', auth_views.password_change, {
		'post_change_redirect': '/accounts/password_change_done',
		'template_name': 'accounts/password_change.html'}),
	url(r'^password_change_done$', auth_views.password_change_done, {
		'template_name': 'accounts/password_change_done.html'
		}),
	url(r'^$', views.my_account),
	url(r'^create$', views.create_account),
	url(r'^account/(?P<id_user>\d+)$', views.view_account, name='view_account'),

]
