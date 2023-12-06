from django.db import models

# Create your models here.

class Cycle(models.Model):
    nom = models.CharField(max_length=255)
    credit_total = models.IntegerField()


    def __str__(self) -> str:
        return "Cycle - " + self.nom
