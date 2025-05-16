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
        name = request.POST.get('ename')
        id_number = request.POST.get('idno')
        rate = request.POST.get('erate')
        allowance = request.POST.get('allowance')
        if allowance != "":
            employee = Employee.objects.create(name=name, id_number=id_number, rate=rate, allowance=allowance)
            employee.save()
            messages.success(request, 'Employee added successfully!')
        if allowance == "":
            employee = Employee.objects.create(name=name, id_number=id_number, rate=rate)
            employee.save()
            messages.success(request, 'Employee added successfully!')
        return redirect('home', pk = pk)
    else:
        user = get_object_or_404(Accounts, pk = pk)
        return render(request, 'payroll_app/add_employee.html', {'user': user})
    
def updateEmployee(request, pk, employee_pk):
    if request.method == "POST":
        name = request.POST.get('ename')
        id_number = request.POST.get('idno')
        rate = request.POST.get('erate')
        allowance = request.POST.get('allowance')
        employee = Employee.objects.get(pk=employee_pk)
        employee.name = name
        employee.id_number = id_number
        employee.rate = rate
        if allowance != "":
            employee.allowance = allowance
        if allowance == "":
            employee.allowance = None
        employee.save()
        messages.success(request, 'Employee updated successfully!')
        return redirect('home', pk = pk)
    else:
        user = get_object_or_404(Accounts, pk = pk)
        employee = get_object_or_404(Employee, pk = employee_pk)
        return render(request, 'payroll_app/update_employee.html', {'user': user, 'employee': employee})

def updateOvertime(request, pk, employee_pk):
    if request.method == "POST":
        overtime_hours = request.POST.get('overtime_hours')
        employee = get_object_or_404(Employee, pk=employee_pk)
        if overtime_hours == "":
            messages.warning(request, 'Please enter overtime hours!')
            return redirect('home', pk=pk)
        elif int(overtime_hours) <= 0:
            messages.warning(request, 'Please enter overtime hours!')
            return redirect('home', pk=pk)
        else:
            employee.overtime_pay = float((int(employee.rate)/160)*1.5*int(overtime_hours))
        employee.save()
        messages.success(request, f"Overtime updated for {employee.name}!")
        return redirect('home', pk=pk)

def deleteEmployee(request, pk, employee_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    employee.delete()
    messages.success(request, 'Employee deleted successfully!')
    return redirect('home', pk=pk)