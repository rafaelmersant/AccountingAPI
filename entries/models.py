from django.db import models

from administration.models import Concept, Church, Person, User

class Entry(models.Model):
    church = models.ForeignKey(Church, on_delete=models.SET_NULL, null=True, blank=True)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True)
    note = models.CharField(max_length=255, blank=True)
    period_year = models.PositiveSmallIntegerField()
    period_month = models.PositiveSmallIntegerField()
    total_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.id}'
 

class Item(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    concept = models.ForeignKey(Concept, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2, null=True)
    reference = models.CharField(max_length=255, blank=True, null=True)
    period_year = models.PositiveSmallIntegerField()
    period_month = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=1, default="E") #E = Entrada / S = Salida
    method = models.CharField(max_length=1, default="E") #E = Efectivo / D = Deposito / R = Retenido
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return f'{self.id}'