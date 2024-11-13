from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Customer(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self) -> str:
        return f'{self.name}'

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    customer_name = models.ForeignKey(Customer,on_delete=models.CASCADE,blank=False,related_name='projects')
    saved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.project_name}'

class Style(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    style_img = models.CharField(max_length=2000, blank=True)
    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name='orders')
    qty = models.IntegerField(null=False, default=100)
    date = models.DateField(default=timezone.now)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='orders')

    def __str__(self) -> str:
        return f'Order:{self.id}'

class Fabric(models.Model):
    code = models.CharField(max_length=100, primary_key=True, blank=True)
    name = models.CharField(max_length=100)
    weight = models.IntegerField()
    ply_height = models.IntegerField()
    cutting_speed = models.IntegerField()
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f'{self.name}{self.weight}'
        super(Fabric, self).save(*args, **kwargs)
    def __str__(self):
        return f'Fabric: {self.code}'

class StyleFabric(models.Model):
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name='style_fabrics')
    material_comp = models.CharField(max_length=1, choices=[
        ('A', 'Fabric A'),
        ('B', 'Fabric B'),
        ('C', 'Fabric C'),
        ('D', 'Fabric D'),
    ])
    material = models.ForeignKey(Fabric, on_delete=models.CASCADE, related_name='style_fabrics', null=True)
    perimeter = models.IntegerField(null=True)
    avg_consumption = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.style.name} uses {self.material} as Fabric {self.material_comp}'


    
