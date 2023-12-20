from django.db import models

# Create your models here.

from utilisateur.models import Utilisateur
from cycle.models import Cycle

class Facture(models.Model):
    etudiant = models.ForeignKey(Utilisateur,on_delete=models.DO_NOTHING)
    cycle = models.ForeignKey(Cycle,on_delete=models.DO_NOTHING)
    montant = models.FloatField()
