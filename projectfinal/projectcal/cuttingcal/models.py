from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Customer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'Customer: {self.name}'

class Factory(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='factories')

    def __str__(self) -> str:
        return f'Customer: {self.customer} - Factory: {self.name} - Site: {self.location}'

class Project(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='projects')

    def __str__(self) -> str:
        return f'Project: {self.code} - {self.name}'

class Fabric(models.Model):
    code = models.CharField(max_length=100, primary_key=True)
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
    fabric = models.ForeignKey(Fabric, on_delete=models.CASCADE, related_name='fabric_styles')
    fabric_comp = models.CharField(max_length=1, choices=[
        ('A', 'Fabric A'),
        ('B', 'Fabric B'),
        ('C', 'Fabric C'),
        ('D', 'Fabric D'),
    ])
    perimeter = models.IntegerField()
    code = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f'{self.fabric.type}{self.fabric.weight}'
        super(StyleFabric, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.style.name} uses {self.fabric} as Fabric {self.fabric_comp}'

class Order(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name='orders')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='orders')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f'Order:{self.id}'

class Size(models.Model):
    size = models.CharField(max_length=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='sizes')

    def __str__(self) -> str:
        return f'Order:{self.order.id} Size:{self.size}'
