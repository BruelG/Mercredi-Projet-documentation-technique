from django.db import models

from cycle.models import Cycle
from programme.models import Programme

from utilisateur.models import Utilisateur

from session.models import Session

# Create your models here.

class Cours(models.Model):
    nom = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    cycle = models.ForeignKey(Cycle,on_delete=models.DO_NOTHING)
    programme = models.ForeignKey(Programme,on_delete=models.DO_NOTHING)
    prerequis = models.ManyToManyField('self', through='Prerequis',
                                           symmetrical=False,
                                           related_name='related_to',blank=True)
    credit = models.IntegerField()
    nom_prof = models.CharField(max_length=255)
    dispenseEn = models.IntegerField()

    def __str__(self) -> str:
        return f"ID : {self.id} - {self.nom}"
    

class Prerequis(models.Model):
    from_cours = models.ForeignKey(Cours, related_name='from_cours',on_delete=models.DO_NOTHING)
    to_cours = models.ForeignKey(Cours, related_name='to_cours',on_delete=models.DO_NOTHING)


class Cours_Etudiants(models.Model):
    cours = models.ForeignKey(Cours,on_delete=models.DO_NOTHING)
    etudiant = models.ForeignKey(Utilisateur,on_delete=models.DO_NOTHING)
    credit = models.IntegerField(default=-1)
    date_inscription = models.DateTimeField()
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)

class Cours_Session(models.Model):
    session = models.ForeignKey(Session,on_delete=models.DO_NOTHING)
    cours = models.ForeignKey(Cours,on_delete=models.DO_NOTHING)
    date_debut = models.DateField()
    date_ase = models.DateField()
