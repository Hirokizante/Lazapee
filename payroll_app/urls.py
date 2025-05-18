from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('register', views.register, name='register'),
    path('home/<int:pk>/', views.home, name='home'),
    path('add_employee/<int:pk>/', views.addEmployee, name='add_employee'),
    path('update_employee/<int:pk>/<int:employee_pk>/', views.updateEmployee, name='update_employee'),
    path('update_overtime/<int:pk>/<int:employee_pk>/', views.updateOvertime, name='update_overtime'),
    path('delete_employee/<int:pk>/<int:employee_pk>/', views.deleteEmployee, name='delete_employee'),
    path('payslips/<int:pk>/', views.payslips, name='payslips'),
    path('manage_account/<int:pk>/', views.manage_account, name='manage_account'),
    path('change_password/<int:pk>/', views.change_password, name='change_password'),
    path('delete_account/<int:pk>/', views.delete_account, name='delete_account'),
    path('logout/', views.logout_view, name='logout'),
    path('view_payslip/<int:pk>/<int:payslip_pk>/', views.view_payslip, name='view_payslip'),
]