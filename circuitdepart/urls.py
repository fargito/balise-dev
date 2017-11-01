from django.conf.urls import url
# cette partie n'est accessible qu'aux admins et kessiers ainsi au'à Zaza
# elle permet de vérifier pour une promotion les élèves qui ont encore des binets à faire passer

from . import views

urlpatterns = [
	url(r'^$', views.circuitdepart_home),
	url(r'^refresh_all/', views.refresh_all, name='refresh_circuitdepart'),
	url(r'^promotion/(?P<promotion>\d+)$', views.recapitulatif_promo, name='circuitdepart'),
	url(r'^sign_unsign/(?P<eleve_id>\d+)$', views.fiche_sign_unsign, name='fiche_sign_unsign'),
	url(r'^promotion/add_problem/', views.add_problem),
	url(r'^mark_as_resolved/(?P<id_problem>\d+)$', views.mark_as_resolved, name='mark_problem_as_resolved'),

]