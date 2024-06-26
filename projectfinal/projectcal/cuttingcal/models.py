from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Customer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'Customer: {self.name}'

class Fabric(models.Model):
    code = models.CharField(max_length=100, primary_key=True, blank=True)
    type = models.CharField(max_length=100)
    weight = models.IntegerField()
    ply_height = models.IntegerField()
    cutting_speed = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f'{self.type}{self.weight}'
        super(Fabric, self).save(*args, **kwargs)

    def __str__(self):
        return f'Fabric: {self.code}'

class Style(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return f'Style: {self.name}'

class StyleFabric(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name='style_fabrics')
    fabric_code = models.ForeignKey(Fabric, on_delete=models.CASCADE, related_name='fabric_styles')
    fabric_comp = models.CharField(max_length=1, choices=[
        ('A', 'Fabric A'),
        ('B', 'Fabric B'),
        ('C', 'Fabric C'),
        ('D', 'Fabric D'),
    ])
    perimeter = models.IntegerField(null=True)
    avg_consumption = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.style.name} uses {self.fabric} as Fabric {self.fabric_comp}'

class Order(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name='orders')
    project = models.CharField(max_length=15, blank=False)
    date = models.DateField(default=timezone.now)

    def __str__(self) -> str:
        return f'Order:{self.id}'
    

class Size(models.Model):
    size = models.CharField(max_length=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='sizes')
    qty = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'Order:{self.order.id} Size:{self.size}'
