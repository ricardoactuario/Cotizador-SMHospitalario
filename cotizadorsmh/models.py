from django.db import models

# Create your models here.

class TR3(models.Model):
    Age = models.IntegerField()
    P50 = models.DecimalField(max_digits=30, decimal_places=25)
    P100 = models.DecimalField(max_digits=30, decimal_places=25)
    P250 = models.DecimalField(max_digits=30, decimal_places=25)
    P500 = models.DecimalField(max_digits=30, decimal_places=25)
    P1000 = models.DecimalField(max_digits=30, decimal_places=25)
    