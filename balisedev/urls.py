from django.conf.urls import url, include
from django.contrib import admin
from compta import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^compta/$', include('blog.urls')),
]
