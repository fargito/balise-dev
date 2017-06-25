from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^home$', views.home),
    url(r'^date$', views.date_actuelle),
    url(r'^addition/(?P<nombre1>\d+)/(?P<nombre2>\d+)/$', views.addition),
    url(r'^accueil$', views.accueil, name = 'accueil'),
    url(r'^article/(?P<id>\d+)-(?P<slug>.+)$', views.lire, name = 'lire'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^article_form/$', views.article_form, name='article_form'),
	url(r'^faq$', views.FAQView.as_view()),   # Nous demandons la vue correspondant à la classe FAQView
]