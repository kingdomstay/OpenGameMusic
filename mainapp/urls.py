from django.template.defaulttags import url
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.TracksListView.as_view(), name='index'),
    path('tracks/<int:pk>', views.TracksDetailView.as_view(), name='track-detail'),
    path('upload/', views.upload, name='upload'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.TracksSearchView.as_view(), name='search'),
    path('likes/<int:ids>', views.like, name='like')
]