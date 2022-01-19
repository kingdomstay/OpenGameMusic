from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout')
]