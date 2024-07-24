from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('<str:short_url>/', views.redirect_url, name='redirect_url'),

    path('delete/<int:url_id>/', views.delete_url, name='delete_url'),
]
