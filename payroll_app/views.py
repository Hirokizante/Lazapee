from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Accounts, Employee

# Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Accounts.objects.filter(username=username, password=password).exists():
            account = Accounts.objects.get(username=username, password=password)
            account_pk = account.pk
            return redirect('home', pk = account_pk)
        else:
            messages.warning(request, 'Invalid credentials!')
            return render(request, 'payroll_app/login.html')
    else:
        return render(request, 'payroll_app/login.html')
    
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if Accounts.objects.filter(username=username).exists():
            messages.warning(request, 'Account already exists!')
            return render(request, 'payroll_app/register.html')
        else:
            Accounts.objects.create(username=username, password=password)
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        return render(request, 'payroll_app/register.html')
    
def home(request, pk):
    employee_objects = Employee.objects.all()
    user = get_object_or_404(Accounts, pk = pk)
    return render(request, 'payroll_app/home.html', {'employees': employee_objects, 'user': user})

def addEmployee(request, pk):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        salary = request.POST.get('salary')
        employee = Employee.objects.create(name=name, email=email, phone=phone, address=address, salary=salary)
        employee.save()
        messages.success(request, 'Employee added successfully!')
        return redirect('home', pk = pk)
    else:
        user = get_object_or_404(Accounts, pk = pk)
        return render(request, 'payroll_app/add_employee.html', {'user': user})