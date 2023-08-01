from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns for your app
    path('register/', views.register, name='register'),
    path('dashboard/' , views.dashboard,name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]
