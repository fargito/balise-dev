from django.conf.urls import url, include
from django.contrib import admin
from accounts import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^compta/', include('compta.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^binets/', include('binets.urls')),
    url(r'^backend/', include('backend.urls')),
    url(r'^vos/', include('vos.urls')),
    url(r'^$', views.home),
    url(r'error^$', views.error),

]
