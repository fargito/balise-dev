from django.conf.urls import url
# cette partie n'est accessible qu'aux admins et kessiers
# elle permet la création d'utilisateurs via import excel
# ainsi que des fonctionnalités de mailing list

from . import views

urlpatterns = [
	url(r'^$', views.backend_home),
	url(r'^import_eleves/$', views.import_eleves),
	url(r'^import_binets/$', views.import_binets),
	url(r'^import_subventions/$', views.import_subventions),
	url(r'^import_liste_binets_officielle/$', views.import_liste_binets_officielle),
	url(r'^export_mailing_lists/$', views.export_mailing_lists),
	url(r'^export_mailing_lists/actifs/$', views.export_mailing_lists_actifs),
	url(r'^export_mailing_lists/promotion/(?P<promo>\d+)$', views.export_mailing_lists_promotion),
	url(r'^export_mailing_lists/actifs/(?P<promo>\d+)$', views.export_mailing_lists_promotion_actifs),
]