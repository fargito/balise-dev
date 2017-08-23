from django.conf.urls import url

from . import views



urlpatterns = [
	url(r'^$', views.subventions_home),
	url(r'^vague/(?P<id_vague>\d+)$', views.view_vague, name='view_vague'),
	url(r'^verser_subvention/(?P<id_subvention>\d+)$', views.verser_subvention, name='verser_subvention'),

]