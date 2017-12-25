from django.conf.urls import url

from . import views


urlpatterns = [
	url(r'^$', views.help_home, name='help_home'),
	url(r'^(?P<filename>[\w\_]+)/$', views.open_file),
]