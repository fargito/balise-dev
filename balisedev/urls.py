from django.conf.urls import url, include
from django.contrib import admin
from accounts import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^compta/', include('compta.urls')),
    url(r'^accounts/', include('accounts.urls')),
    #url(r'^blog/', include('blog.urls')),
    url(r'^$', views.home),

]
