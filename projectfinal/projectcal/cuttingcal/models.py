from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Customer(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self) -> str:
        return f'Customer name: {self.name}'

class Factory(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='factories')
    def __str__(self) -> str:
        return f'Customer: {self.customer} - Factory: {self.name} - Site: {self.location}'

class Project(models.Model):
    code = models.CharField(max_length=10,primary_key=True)
    name = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='projects')
    def __str__(self) -> str:
        return f'Project: {self.code} Customer: {self.customer}'

class Fabric(models.Model):
    type = models.CharField(max_length=20)
    weight = models.IntegerField()
    ply_height = models.IntegerField()

class Style(models.Model):
    name = models.CharField(max_length=50)
    fabric_A = models.ForeignKey(Fabric, on_delete=models.CASCADE, related_name='Astyles')
    fabric_B = models.ForeignKey(Fabric, on_delete=models.CASCADE, related_name='Bstyles')
    fabric_C = models.ForeignKey(Fabric, on_delete=models.CASCADE, related_name='Cstyles')

class Order(models.Model):
    size_set = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='orders')
    style = models.ForeignKey(Style, on_delete=models.CASCADE, related_name='orders')
    