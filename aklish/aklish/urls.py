"""
URL configuration for aklish project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("users/", include("users.urls")),
    path("translate/", include("translate.urls")),
    path("dictionary/", include("dictionary.urls")),
    path("dictionary/api/", include("dictionary.api.urls")),
    path("proofreader/", include("proofreader.urls")),
    path("proofreader/api/", include("proofreader.api.urls")),
    path("games/", include("games.urls")),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
