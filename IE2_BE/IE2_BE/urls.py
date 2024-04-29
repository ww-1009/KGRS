"""IE2_BE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from app import views

urlpatterns = [
	path('admin/', admin.site.urls),
	path('nasdaq/newstop/', views.getnewstop),
	path('nasdaq/entitydata/', views.get_fd_group),
	path('nasdaq/graphinfolist/', views.get_self_graph_info),
	path('nasdaq/selfentitylist/', views.get_self_entity_info),
	path('nasdaq/selfrelationlist/', views.get_self_relation_info),
	path('nasdaq/selfgraph/', views.get_self_graph),
	path('nasdaq/savegraphinfo/', views.save_self_graph_info),
	path('nasdaq/saveentityinfo/', views.save_self_entity_info),
	path('nasdaq/saverelationinfo/', views.save_self_relation_info),
	path('nasdaq/collectinfolist/', views.get_collect_list),
	path('nasdaq/changecollect/', views.change_collect),

]
