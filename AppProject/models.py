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
        count = 0
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
    total = models.FloatField(default=0.00)

    def save(self, *args, **kwargs):
        if self.rent_start and self.rent_end and self.car.gear and self.car.car_cc:
            duration = (self.rent_end - self.rent_start).days if self.rent_end else 1
            if self.car.gear == 'manual':
                gear_rate = 300
            else:
                gear_rate = 600
            if self.car.car_cc == '125':
                cc_rate = 300
            elif self.car.car_cc == '150':
                cc_rate = 600
            elif self.car.car_cc == '300':
                cc_rate = 900
            else:
                cc_rate = 1200
            self.total = duration * (gear_rate + cc_rate)
        super(RentalOrder, self).save(*args, **kwargs)

class RentalReture(models.Model):
    id = models.AutoField(primary_key=True)
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE, default=None)
    cus_id = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    reture_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super(RentalReture, self).save(*args, **kwargs)

        if self.car_id:
            self.car_id.status = 'Returned'
            self.car_id.save()

class DailyReport(models.Model):
    date = models.DateField()
    ren_count = models.IntegerField(default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
