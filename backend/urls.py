from django.conf.urls import url
# cette parti n'est accessible qu'aux admins et kessiers
# elle permet la création d'utilisateurs via import excel

from . import views

urlpatterns = [
	url(r'^$', views.backend_home),
	url(r'^import_eleves/$', views.import_eleves),
	url(r'^import_binets/$', views.import_binets),
	url(r'^import_subventions/$', views.import_subventions),
	url(r'^import_liste_binets_officielle/$', views.import_liste_binets_officielle),
]