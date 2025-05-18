from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    id_number = models.CharField(max_length=20, unique=True)
    rate = models.FloatField()
    overtime_pay = models.FloatField(null=True, blank=True)
    allowance = models.FloatField(null=True, blank=True)
    def getName(self):
        return self.name
    def getID(self):
        return self.id_number
    def getRate(self):
        return self.rate
    def getOvertime(self):
        return self.overtime_pay
    def getAllowance(self):
        return self.allowance
    def resetOvertime(self):
        self.overtime_pay = 0
        self.save()
    def __str__(self):
        return f"{self.pk}: {self.id_number}, rate: {self.salary_rate}"
class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)
    date_range = models.CharField(max_length=50)
    year = models.CharField(max_length=4)
    pay_cycle = models.PositiveIntegerField()
    rate = models.FloatField()
    earnings_allowance = models.FloatField()
    deductions_tax = models.FloatField()
    deductions_health = models.FloatField()
    pag_ibig = models.FloatField()
    sss = models.FloatField()
    overtime = models.FloatField()
    total_pay = models.FloatField()
    def getIDNumber(self):
        return self.employee.id_number
    def getMonth(self):
        return self.month
    def getDateRange(self):
        return self.date_range
    def getYear(self):
        return self.year
    def getPayCycle(self):
        return self.pay_cycle
    def getRate(self):
        return self.rate
    def getCycleRate(self):
        return self.rate / 2
    def getEarningsAllowance(self):
        return self.earnings_allowance
    def getTaxDeductions(self):
        return self.deductions_tax
    def getHealthDeductions(self):
        return self.deductions_health
    def getPagIbig(self):
        return self.pag_ibig
    def getSSS(self):
        return self.sss
    def getOvertime(self):
        return self.overtime
    def getTotalPay(self):
        return self.total_pay
    def __str__(self):
        return f"PK: {self.pk}, Employee: {self.employee.id_number}, Period: {self.month} {self.date_range}, {self.year}, Cycle: {self.pay_cycle}, Total Pay: {self.total_pay}"
class Accounts(models.Model):
    username = models.CharField(max_length=300)
    password = models.CharField(max_length=300)
    def getUsername():
        return Accounts.username
    def getPassword():
        return Accounts.password
    def __str__(self):
        return f"{Accounts.username}"