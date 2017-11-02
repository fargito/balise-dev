from django.conf.urls import url
from django.views.generic import ListView

from . import views
from .models import Binet

urlpatterns = [
	url(r'^$', views.all_binets, name='liste_binets'),
	url(r'^new_binet$', views.new_binet, name='new_binet'),
	url(r'^binet_hide_unhide/(?P<id_binet>\d+)$', views.binet_hide_unhide, name='binet_hide_unhide'),
	url(r"^history/(?P<id_binet>\d+)$", views.binet_history, name='binet_history'),
	url(r"^edit/(?P<id_binet>\d+)$", views.edit_binet, name='edit_binet'),
	url(r"^edit/(?P<id_binet>\d+)/new_mandat$", views.new_mandat, name='new_mandat'),
	url(r"^edit/(?P<id_binet>\d+)/mandat/(?P<id_mandat>\d+)$", views.edit_mandat, name='edit_mandat'),
	url(r"^last_not_last/(?P<id_mandat>\d+)$", views.mandat_last_not_last, name='mandat_last_not_last'),	
	url(r"^activate_deactivate/(?P<id_mandat>\d+)$", views.mandat_activate_deactivate, name='mandat_activate_deactivate'),	
	url(r"^touch_untouch/(?P<id_mandat>\d+)$", views.mandat_touch_untouch, name='mandat_touch_untouch'),
	url(r'^export_binets_list$', views.export_binets_list, name='export_binets_list'),
]