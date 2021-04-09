from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('users/create', views.create_user),
    path('ideas_page', views.ideas),
    path('users/login', views.login),
    path('logout', views.logout),
    path('idea/create', views.create_idea)
]