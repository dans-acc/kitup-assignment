"""kitup_project URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.urls import include

# For setting up dynamic media - uploads by the user.
from django.conf import settings
from django.conf.urls.static import static

# Import views from the projects
from kitup import views as kitup_app_views

# Redirects anything that does not start with anything.
# Mapping checks for URL beginnings.
# When a match is made, the remainder of the URL string is passed and
# handled by the appropriate apps 'urls.py' module.
# This is achieved by the include function.
urlpatterns = [
    path('', include('kitup.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
