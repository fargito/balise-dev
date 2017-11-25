from django.conf.urls import url

from . import views


urlpatterns = [
	url(r'^$', views.passations_home, name='passations_home'),
	url(r'^promotion/(?P<promotion>\d+)$', views.recapitulatif_promo, name='passation'),
	url(r'^bilan/(?P<id_mandat>\d+)$', views.mandat_bilan, name='mandat_bilan'),
	url(r'^promo_bilan/(?P<promotion>\d+)$', views.promotion_bilan, name='promo_bilan'),

]