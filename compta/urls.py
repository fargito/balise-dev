from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^$', views.my_binets),
    url(r"^journal/(?P<id_mandat>\d+)$", views.mandat_set, name='mandat_journal'),
	url(r'^journal/$', views.mandat_journal),
    url(r'^journal/delete_ligne/(?P<id_ligne>\d+)$', views.delete_ligne, name='delete_ligne'),
    url(r'^journal/edit_ligne/(?P<id_ligne>\d+)$', views.edit_ligne, name='edit_ligne'),
    url(r'^journal/view_ligne/(?P<id_ligne>\d+)$', views.view_ligne, name='view_ligne'),
    url(r'^journal/kick_ligne/(?P<id_ligne>\d+)$', views.kick_ligne, name='kick_ligne'),
    url(r'^journal/pass_ligne_to_next/(?P<id_ligne>\d+)$', views.pass_ligne_to_next, name='pass_ligne_to_next'),
    url(r'^journal/pass_ligne_to_previous/(?P<id_ligne>\d+)$', views.pass_ligne_to_previous, name='pass_ligne_to_previous'),
    url(r'^journal/lock_unlock_ligne/(?P<id_ligne>\d+)$', views.lock_unlock_ligne, name='lock_unlock_ligne'),
    url(r'^journal/check_uncheck_ligne/(?P<id_ligne>\d+)$', views.check_uncheck_ligne, name='check_uncheck_ligne'),
    url(r'^journal/lock_unlock_ligne_polymedia/(?P<id_ligne>\d+)$', views.lock_unlock_ligne_polymedia, name='lock_unlock_ligne_polymedia'),
    url(r'^journal/lock_unlock_all/$', views.lock_unlock_all, name='lock_unlock_all'),
    url(r'^journal/create_poste_depense/$', views.create_poste_depense),
    url(r'^journal/edit_poste_depense/(?P<id_poste>\d+)$', views.edit_poste_depense, name='edit_poste_depense'),
    url(r'^journal/delete_poste_depense/(?P<id_poste>\d+)$', views.delete_poste_depense, name='delete_poste_depense'),
    url(r'^journal/create_evenement/$', views.create_evenement),
    url(r'^journal/edit_evenement/(?P<id_evenement>\d+)$', views.edit_evenement, name='edit_evenement'),
    url(r'^journal/delete_evenement/(?P<id_evenement>\d+)$', views.delete_evenement, name='delete_evenement'),
    url(r'^view_remarques/$', views.view_remarques),
    url(r'^binet_subventions/$', views.binet_subventions, name='binet_subventions'),
    url(r'^binet_compta_history/$', views.binet_compta_history),
    url(r'^import_lignes/$', views.import_lignes),
    url(r'^seance_cheques$', views.seance_cheques, name='seance_cheques'),
    url(r'^polymedia$', views.validate_polymedia, name='validate_polymedia'),
    url(r'^bilan/$', views.binet_bilan),
    url(r'^operations/$', views.all_operations, name='all_operations'),
    url(r'^operations/(?P<operation_id>\d+)$', views.operation_details, name='operation_details'),
    url(r'^operations/create', views.create_operation, name='create_operation'),
]
