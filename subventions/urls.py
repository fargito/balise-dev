from django.conf.urls import url

from . import views



urlpatterns = [
	url(r'^$', views.subventions_home),
	url(r'^vague/(?P<id_vague>\d+)$', views.view_vague, name='view_vague')

]