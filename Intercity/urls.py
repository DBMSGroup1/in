"""
URL configuration for Intercity project.

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
from django.urls import path
from . import views

urlpatterns = [
	path('admin/', admin.site.urls),
	path('user_log',views.user_log,name='index'),
	path('index',views.index,name='index'),
	path('register',views.register,name="register"),
	path('agent_log',views.agent_log,name="agent_login"),
    path('user_reg',views.user_reg,name='user_reg'),
    path('agent_reg',views.agent_reg,name='agen_reg'),
    path('logout',views.logout,name='logout'),
    path('home',views.home,name='home'),
    path('schedule',views.schedule,name='logout'),
    path('login',views.login,name='login'),
    path('',views.start,name='login'),
    
]
