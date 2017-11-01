from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^$', views.my_binets),
    url(r"^journal/(?P<id_mandat>\d+)$", views.mandat_set, name='mandat_journal'),
	url(r'^journal/$', views.mandat_journal),
    url(r'^journal/delete_ligne/(?P<id_ligne>\d+)$', views.delete_ligne, name='delete_ligne'),
    url(r'^journal/edit_ligne/(?P<id_ligne>\d+)$', views.edit_ligne, name='edit_ligne'),
    url(r'^journal/view_ligne/(?P<id_ligne>\d+)$', views.view_ligne, name='view_ligne'),
    url(r'^journal/lock_unlock_ligne/(?P<id_ligne>\d+)$', views.lock_unlock_ligne, name='lock_unlock_ligne'),
    url(r'^journal/lock_unlock_ligne_polymedia/(?P<id_ligne>\d+)$', views.lock_unlock_ligne_polymedia, name='lock_unlock_ligne_polymedia'),
    url(r'^journal/lock_unlock_all/$', views.lock_unlock_all, name='lock_unlock_all'),
    url(r'^journal/create_poste_depense/$', views.create_poste_depense),
    url(r'^journal/delete_poste_depense/(?P<id_poste>\d+)$', views.delete_poste_depense, name='delete_poste_depense'),
    url(r'^view_remarques/$', views.view_remarques),
    url(r'^binet_subventions/$', views.binet_subventions, name='binet_subventions'),
    url(r'^binet_compta_history/$', views.binet_compta_history),
    url(r'^import_lignes/$', views.import_lignes),
    url(r'^seance_cheques$', views.seance_cheques, name='seance_cheques'),
    url(r'^polymedia$', views.validate_polymedia, name='validate_polymedia'),
    url(r'^bilan/$', views.binet_bilan),

]
