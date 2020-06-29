"""Food URL Configuration

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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

import order
from account import views as login_view
from menu import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('register/', login_view.register, name='register'),
                  path('profile/', login_view.AccountDetailView.as_view(), name='profile'),
                  path('update/', login_view.AccountUpdateView.as_view(), name='accountupdate'),
                  path('menu/', include('menu.urls')),
                  path('donhang/', views.don_hang_view, name='donhang'),
                  path('customer-report/', views.customer_report_view, name='customer-report'),
                  path('report/', views.report_view, name='report'),
                  path('cart/', include('order.urls')),
                  url('login/', LoginView.as_view(template_name='login/login.html'), name='login'),
                  url('logout/', LogoutView.as_view(template_name='login/logout.html'), name='logout'),
                  url(r'^$', include('home.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
