from django.db import models

from administration.models import Concept, Church, Person, User

class Entry(models.Model):
    concept = models.ForeignKey(Concept, on_delete=models.SET_NULL, null=True)
    church = models.ForeignKey(Church, on_delete=models.SET_NULL, null=True)
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=18, decimal_places=2, null=True)
    reference = models.CharField(max_length=255)
    type = models.CharField(max_length=1, default="E")
    period_month = models.PositiveSmallIntegerField()
    period_year = models.PositiveSmallIntegerField()
    created_date = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'{self.id}'