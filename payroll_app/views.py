from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Accounts, Employee, Payslip

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
        if Employee.objects.filter(id_number=id_number).exists():
            messages.warning(request, 'Employee ID already exists!')
            return redirect('home', pk = pk)
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

def payslips(request, pk):
    if request.method == "POST":
        employee_pk = request.POST.get('employee')  
        month = request.POST.get('month')
        date_range = request.POST.get('daterange')
        year = request.POST.get('year')
        pay_cycle = request.POST.get('cycle')
        employee = get_object_or_404(Employee, pk=employee_pk)
        if Payslip.objects.filter(employee=employee, pay_cycle=pay_cycle, month=month, date_range=date_range, year=year).exists():
            messages.warning(request, 'Payslip already exists for this employee and pay cycle!')
            return redirect('payslips', pk=pk)
        else:
            pag_ibig = 100
            philhealth = employee.rate * 0.04
            sss = employee.rate * 0.045
            allowance = employee.allowance or 0
            overtime = employee.overtime_pay or 0
            deductions_tax = ((employee.rate / 2) + allowance + overtime - pag_ibig) * 0.2
            deductions_health = ((employee.rate / 2) + allowance + overtime - philhealth - sss) * 0.2
            total_pay = 0
            if pay_cycle == "1":
                total_pay = ((employee.rate / 2) + allowance + overtime - pag_ibig) - deductions_tax
            elif pay_cycle == "2":
                total_pay = ((employee.rate / 2) + allowance + overtime - philhealth - sss) - deductions_health
            payslip = Payslip.objects.create(
                employee=employee,
                month=month,
                date_range=date_range,
                year=year,
                pay_cycle=pay_cycle,
                rate=employee.rate,
                earnings_allowance=allowance,
                deductions_tax=deductions_tax,
                deductions_health=deductions_health,
                pag_ibig=pag_ibig,
                sss=sss,
                overtime=overtime,
                total_pay=total_pay
            )
            payslip.save()
            messages.success(request, 'Payslip created successfully!')
            return redirect('payslips', pk=pk)
    else:
        user = get_object_or_404(Accounts, pk=pk)
        employees = Employee.objects.all()
        payslips = Payslip.objects.all()
        return render(request, 'payroll_app/payslips.html', {'user': user, 'employees': employees, 'payslips': payslips})

def manage_account(request, pk):
    user = get_object_or_404(Accounts, pk=pk)
    return render(request, 'payroll_app/manage_account.html', {'user': user})

def change_password(request, pk):
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        user = get_object_or_404(Accounts, pk=pk)
        
        if old_password != user.password:
            messages.warning(request, 'Current password is incorrect!')
            return render(request, 'payroll_app/change_password.html', {'user': user})
        
        if new_password != confirm_password:
            messages.warning(request, 'New password and confirm password do not match!')
            return render(request, 'payroll_app/change_password.html', {'user': user})
        
        user.password = new_password
        user.save()
        messages.success(request, 'Password changed successfully!')
        return redirect('home', pk=pk)
    else:
        user = get_object_or_404(Accounts, pk=pk)
        return render(request, 'payroll_app/change_password.html', {'user': user})

def delete_account(request, pk):
    if request.method == "POST":
        user = get_object_or_404(Accounts, pk=pk)
        user.delete()
        messages.success(request, 'Account deleted successfully!')
        return redirect('login')
    return redirect('home', pk=pk)

def logout_view(request):
    return redirect('login')

def view_payslip(request, pk, payslip_pk):
    user = get_object_or_404(Accounts, pk=pk)
    payslip = get_object_or_404(Payslip, pk=payslip_pk)
    
    gross_pay = (payslip.rate / 2) + payslip.earnings_allowance + payslip.overtime
    
    if payslip.pay_cycle == 1:
        total_deductions = payslip.deductions_tax + payslip.pag_ibig
    else:
        total_deductions = payslip.deductions_health + payslip.sss + payslip.deductions_tax
    
    context = {
        'user': user,
        'payslip': payslip,
        'gross_pay': gross_pay,
        'total_deductions': total_deductions
    }
    
    return render(request, 'payroll_app/view_payslip.html', context)