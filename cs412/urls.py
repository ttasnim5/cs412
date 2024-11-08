"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hw/", include("hw.urls")), ## we create the URL hw/, and associate it with URLs in another file
    path("quote/", include("quotes.urls")),
    path("formdata/", include("formdata.urls")),
    path("restaurant/", include("restaurant.urls")),
    path("blog/", include("blog.urls")),
    path("mini_fb/", include("mini_fb.urls")),
    path("marathon_analytics/", include("marathon_analytics.urls")),
    path("voter_analytics/", include("voter_analytics.urls")),
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)