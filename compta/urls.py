from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^$', views.my_binets),
    url(r"^journal/(?P<id_mandat>\d+)$", views.mandat_set, name='mandat_journal'),
	url(r'^journal/$', views.mandat_journal),
    
]
