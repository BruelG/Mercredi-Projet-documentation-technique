from django.db import models

from django.contrib.auth.models import PermissionsMixin, Group, Permission
from django.utils.translation import gettext_lazy as _

from cycle.models import Cycle
from session.models import Session
from programme.models import Programme

# Create your models here.

class Utilisateur(models.Model):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    pseudo = models.CharField(max_length=255,primary_key=True)
    mdp = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True)

    cycle = models.ForeignKey(Cycle,on_delete=models.DO_NOTHING)
    programme = models.ForeignKey(Programme,on_delete=models.DO_NOTHING)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)



class UtilisateurSession(models.Model):
    id_session = models.IntegerField(primary_key=True)
    user = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    last_login = models.DateTimeField(auto_now=True)