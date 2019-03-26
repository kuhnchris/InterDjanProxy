"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import re_path, url, include
from reverseproxyapp.views import ReverseProxyView
from portal_praas.views import PraaSPortalView
from django.views.generic import RedirectView
from django.contrib import admin
from django.contrib.auth import urls

urlpatterns = (
    re_path(r'^proxy/(?P<domain>[^/]*)/(?P<path>.*)$', ReverseProxyView.as_view()),
    url(r"user/", include('django.contrib.auth.urls')),
    url(r"login/$",RedirectView.as_view(url="/user/login/")),
    url(r"logout/$",RedirectView.as_view(url="/user/logout/")),
    url(r"accounts/profile/$",RedirectView.as_view(url="/portal/")),
    re_path('admin/', admin.site.urls),
    re_path(r"^$",RedirectView.as_view(url="/portal/")),
    url(r"portal/$",PraaSPortalView.as_view())
)
