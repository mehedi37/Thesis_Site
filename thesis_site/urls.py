"""
URL configuration for thesis_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='project_list')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='project_list')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('api/register/admin/', views.register_admin, name='register_admin'),
    path('', include('project.urls'), name='project_list'),
    path('supervisor/', include('supervisor.urls'), name='supervisor_main_url'),
    path('unit_co/', include('unit_co.urls'), name='unit_co_main_url'),
    path('conversation/', include('chat.urls'), name='chat_main_url'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
