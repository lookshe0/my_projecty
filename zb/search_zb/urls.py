"""
URL configuration for search_zb project.

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
from django.urls import path

from search import views
from search.views import Index

from search.views import article_detail





urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Index.as_view(),name="index"),
    path('article/<int:id>', views.article_detail, name='article_detail'),
    path('sh', views.sh, name='sh'),
    path('bj', views.bj, name='bj'),
    path('oneweek', views.oneweek, name='oneweek'),
    path('onemonth', views.onemonth, name='onemonth'),
    path('threemonths', views.threemonths, name='threemonths'),
    path('halfyear', views.halfyear, name='halfyear'),
    path('oneyear', views.oneyear, name='oneyear'),
    #path('none',view.none,name='none'),
]
