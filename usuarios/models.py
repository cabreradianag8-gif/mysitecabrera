from django.db import models

# Create your models here.
class usuario(models.Model):
    nombre = models.CharField()
    apellido = models.CharField()
    cargo = models.CharField()
    email = models.EmailField()
    password = models.CharField()
