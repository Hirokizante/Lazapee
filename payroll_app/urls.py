from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('home/<int:pk>/', views.home, name='home'),
    path('add_employee/<int:pk>/', views.addEmployee, name='add_employee'),
]