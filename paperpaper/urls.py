"""
URL configuration for paperpaper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='home'), name='admin_logout'),
    path('login/', auth_views.LoginView.as_view(template_name='paperpaper/login.html'), name='login'),
    path('', views.home, name='home'),
    path('search/', views.search_articles, name='search_articles'),
    path('events/', views.events_list, name='events_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<slug:slug>/edit/', views.event_edit, name='event_edit'),
    path('events/<slug:slug>/delete/', views.event_delete, name='event_delete'),
    path('authors/', views.authors_list, name='authors_list'),
    path('notifications/subscribe/', views.notification_subscribe, name='notification_subscribe'),
    path('admin/bibtex-import/', views.bibtex_import, name='bibtex_import'),
    path('<slug:slug>/', views.event_detail, name='event_detail'),
    path('<slug:slug>/<int:year>/', views.edition_detail, name='edition_detail'),
    path('authors/<slug:slug>/', views.author_detail, name='author_detail'),
]

# Servir arquivos de media durante desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
