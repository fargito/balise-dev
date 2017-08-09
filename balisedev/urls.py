from django.conf.urls import url, include
from django.contrib import admin
from accounts import views
from django_cas_ng.views import login, logout


urlpatterns = [
	url(r'^login$', login, name='cas_ng_login'),
	url(r'^logout$', logout, name='cas_ng_logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^compta/', include('compta.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^binets/', include('binets.urls')),
    url(r'^backend/', include('backend.urls')),
    url(r'^subventions/', include('subventions.urls')),
    url(r'^passations/', include('passations.urls')),
    url(r'^vos/', include('vos.urls')),
    url(r'^$', views.home),
    url(r'error^$', views.error),

]
