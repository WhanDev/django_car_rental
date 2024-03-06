from django.utils import timezone
from django.db.models import F, Sum, Count
from django.db import models

class CarBarnd(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return str(self.id) + ":" + self.name

    def getCountCar(self):
        count = Car.objects.filter(brand=self).count()
        return count


Gear_CHOICES = [
    ('manual', 'เกียร์ธรรมดา'),
    ('automatic', 'เกียร์ออโต'),
]

CC_CHOICES = [
    ('125', '125'),
    ('150', '150'),
    ('300', '300'),
    ('650', '650'),
]

Status_CHOICES = [
    ('enable', 'พร้อมให้เช่า'),
    ('disibled', 'ไม่พร้อมให้เช่า'),
]

class Car(models.Model):
    car_id = models.CharField(max_length=5, primary_key=True, default="")
    brand = models.ForeignKey(CarBarnd, on_delete=models.CASCADE, default=None)
    model = models.CharField(max_length=100, default="")
    gear = models.CharField(max_length=20, choices=Gear_CHOICES, default="manual")
    car_cc = models.CharField(max_length=20, choices=CC_CHOICES, default="125")
    status = models.CharField(max_length=20, choices=Status_CHOICES, default="enable")
    picture = models.ImageField(upload_to='static/cars/', default="")

    def __str__(self):
        return str(self.car_id) + ":" + self.brand.name + self.model + self.gear + self.car_cc

    def getCountOrder(self):
        count = RentalOrder.objects.filter(car_id=self).count()
        return count

class Customer(models.Model):
    cus_id = models.CharField(max_length=13, primary_key=True, default="")
    username = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, default="")
    firstname = models.CharField(max_length=100, default="")
    lastname = models.CharField(max_length=100, default="")
    # password
    tell = models.CharField(max_length=10, default="")
    address = models.TextField(default="")

    def __str__(self):
        return str(self.cus_id) + ":" + self.username + "|" + self.email


ROLES = [
    ('employee', 'พนักงาน'),
    ('admin', 'แอดมิน'),
]


class Employ(models.Model):
    em_id = models.CharField(max_length=13, primary_key=True, default="")
    email = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100, default="")
    # password
    tell = models.CharField(max_length=10, default="")
    address = models.TextField(default="")
    role = models.CharField(max_length=20, choices=ROLES, default="")

    def __str__(self):
        return str(self.em_id) + ":" + self.name + "|" + self.email


class RentalOrder(models.Model):
    id = models.AutoField(primary_key=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    cus_id = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    ren_start = models.DateField()
    ran_end = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, default="รอการชำระเงิน")
    total = models.FloatField(default=0.00)
    #ยกเลิกรายการเช่า


class RentalPayment(models.Model):
    id = models.AutoField(primary_key=True)
    rental_id = models.ForeignKey(RentalOrder, on_delete=models.CASCADE, default=None)
    date_payment = models.DateTimeField(default=timezone.now)
    bill = models.ImageField(upload_to='static/bills/', default="")
    #ชำระเงินแล้ว

class RentalService(models.Model):
    id = models.AutoField(primary_key=True)
    rental_id = models.ForeignKey(RentalOrder, on_delete=models.CASCADE, default=None)
    date_service = models.DateTimeField(default=timezone.now)
    #รับรถไปใช้งานแล้ว

class RentalReture(models.Model):
    id = models.AutoField(primary_key=True)
    rental_id = models.ForeignKey(RentalOrder, on_delete=models.CASCADE, default=None)
    date_reture = models.DateTimeField(default=timezone.now)
    #ส่งคืนรถแล้ว

class DailyReport(models.Model):
    date = models.DateField()
    ren_count = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
