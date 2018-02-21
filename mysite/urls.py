"""mysite URL Configuration."""

from django.conf.urls import url, include
from django.contrib import admin

from django.contrib.auth import views

from .settings import LOGIN_REDIRECT_URL

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout', kwargs={'next_page': LOGIN_REDIRECT_URL}),
    url(r'', include('blog.urls')),
]
