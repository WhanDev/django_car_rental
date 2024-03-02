from django.db import models
from django.db.models import Count

class CarBarnd(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return str(self.id) + ":" + self.name

    def getCountCar(self):
        count = Car.objects.filter(brand=self).count()
        return count


Model_CHOICES = [
        ('car', 'รถยนต์'),
        ('motorcycle', 'มอเตอร์ไซค์'),
    ]
class Car(models.Model):
    car_id = models.CharField(max_length=5, primary_key=True, default="")
    brand = models.ForeignKey(CarBarnd, on_delete=models.CASCADE, default=None)
    model = models.CharField(max_length=100, default="")
    type = models.CharField(max_length=20, choices=Model_CHOICES)
    price = models.FloatField(default=0.00)
    rental_rate = models.DecimalField(max_digits=5, decimal_places=2)
    picture = models.ImageField(upload_to='static/cars/', default="")

    def __str__(self):
        return str(self.car_id) + ":" + self.brand + "|" + self.model

    def getCountOrder(self):
        count = 0
        return count

class Customer(models.Model):
    cus_id = models.CharField(max_length=13, primary_key=True, default="")
    email = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100, default="")
    # password
    tell = models.CharField(max_length=10, default="")
    address = models.TextField(default="")
    role = models.CharField(max_length=20, default="ลูกค้า")

    def __str__(self):
        return str(self.cus_id) + ":" + self.name + "|" + self.email


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


class Rental(models.Model):
    id = models.AutoField(primary_key=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    cus_id = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    ren_start = models.DateField()
    ran_end = models.DateField(null=True, blank=True)
    total = models.FloatField(default=0.00)


class DailyReport(models.Model):
    date = models.DateField()
    ren_count = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
