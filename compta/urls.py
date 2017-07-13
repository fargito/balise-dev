from django.conf.urls import url

from . import views


urlpatterns = [

    url(r'^$', views.my_binets),
    url(r"^journal/(?P<id_mandat>\d+)$", views.mandat_set, name='mandat_journal'),
	url(r'^journal/$', views.mandat_journal),
    url(r'^journal/delete_ligne/(?P<id_ligne>\d+)$', views.delete_ligne, name='delete_ligne'),
    url(r'^journal/edit_ligne/(?P<id_ligne>\d+)$', views.edit_ligne, name='edit_ligne'),
    url(r'^journal/view_ligne/(?P<id_ligne>\d+)$', views.view_ligne, name='view_ligne'),
    url(r'^view_remarques/$', views.view_remarques),
    url(r'^binet_subventions/$', views.binet_subventions),

]
