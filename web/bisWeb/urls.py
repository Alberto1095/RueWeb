"""web URL Configuration

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
from django.urls import path, include
from . import views

urlpatterns = [   
    path('login', views.loginView, name='login'),
    path('logout', views.logoutUser, name='logout'), 
    path('cleanDatabase', views.cleanDatabase, name='cleanDatabase'), 
    path('adminPanel', views.adminView, name='adminView'),   
    path('bisListView', views.bisListView, name='bisListView'),   
    path('initializePlayerItems', views.initializePlayerItems, name='initializePlayerItems'),  
    path('initializeDatabase', views.initializeDatabase, name='initializeDatabase'),  
    path('addOrUpdateItemPicked', views.addOrUpdateItemPicked, name='addOrUpdateItemPicked'),    
    path('removeItemPicked', views.removeItemPicked, name='removeItemPicked'), 
]
