"""NovelAIUser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
import xadmin
from django.urls import path, re_path
from django.urls import include
from Data.views import *
from Data1.views import *
from Config.views import *
from django.views import static
from django.conf.urls import url
from django.conf import settings

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', include('Data.urls')),
    path('', include('Data1.urls')),  path("", Home, name='Home'),  # 主页
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    url(r'^txt2video/(?P<path>.*)$', static.serve, {'document_root': settings.TXT2VIDEO}, name='txt2video'),
]

handler400 = bad_request
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error
