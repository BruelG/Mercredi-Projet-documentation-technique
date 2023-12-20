from django.db import models
from datetime import datetime
from django.conf import settings
from django.utils.html import format_html
import os
from django.urls import reverse
# -------------------------------Table Programme----------------------------------------------------
class Programme(models.Model):
    TITRE_CHOICES = (
        ('Génie logiciel', 'Génie logiciel'),
        ('Développement web', 'Développement web'),
        ('Analyse de données en biologie', 'Analyse de données en biologie'),
        ("Systèmes d'informatique en réseaux", "Systèmes d'informatique en réseaux"),
        ('Méthodes statistiques', 'Méthodes statistiques'),
        ('Mathématiques appliquées', 'Mathématiques appliquées'),
        ('Génie électrique', 'Génie électrique'),
        ('Design industriel', 'Design industriel'),
        ('Sciences politiques', 'Sciences politiques'),
        ('Études en intelligence artificielle', 'Études en intelligence artificielle'),
    )
    TYPE_CHOICES = (
        ('Baccalauréat','Baccalauréat'),
        ('Master','Master'),
        ('Doctorat','Doctorat'),
        ('Maîtrise','Maîtrise')
    )
    CYCLE_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )
    titre = models.CharField(max_length=100, choices=TITRE_CHOICES)
    type_admission = models.CharField(max_length=50, choices=TYPE_CHOICES)
    cycle = models.CharField(max_length=50, choices=CYCLE_CHOICES)
    trimestres = models.ManyToManyField('Trimestre', through='ProgrammeTrimestre', related_name='programmes')
    description = models.TextField()
    credits_programme = models.IntegerField()
    objectifs = models.TextField()
    duree_programme = models.IntegerField()
    prix_Programme = models.FloatField(max_length=8 ,default=36000.00)
    def __str__(self):
            return self.titre
    @classmethod
    def get_all_type_admission(cls):
        types_admission = cls.objects.values_list('type_admission', flat=True).distinct()
        return list(types_admission)
    @classmethod
    def get_programmes_by_type_admission(cls, type_admission):
        programmes = cls.objects.filter(type_admission=type_admission)
        return list(programmes)
# -------------------------------Table Information_Personnelle----------------------------------------------------
class Information_Personnelle(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField() 
    lieu_naissance = models.CharField(blank=True,max_length=256)
    nationalite = models.CharField(max_length=30)
    adresse = models.TextField()
    telephone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    sexe = models.CharField(max_length=8)
    status_Matrimoniale = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    def __str__(self):
        return self.nom + " "+ self.prenom + " "+ str(self.date_naissance)
# -------------------------------Table Trimestre----------------------------------------------------
class Trimestre(models.Model):
    TRIMESTRE_CHOICES = (
        ('Hiver', 'Hiver'),
        ('Été', 'Été'),
        ('Automne', 'Automne'),
    )
    nom = models.CharField(max_length=50, choices=TRIMESTRE_CHOICES)
    annee = models.IntegerField(default=2023) 
 

    def __str__(self):
        return f"{self.nom} {self.annee}"
    @classmethod
    def get_anne_trimest_by_anne(cls,annee):
        trimestre_anne=  cls.objects.filter(annee=annee)
        return trimestre_anne

# -------------------------------Table ProgrammeTrimestre----------------------------------------------------

class ProgrammeTrimestre(models.Model):
    programme = models.ForeignKey(Programme, on_delete=models.CASCADE)
    trimestre = models.ForeignKey(Trimestre, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.programme} {self.trimestre}"
    @classmethod
    def get_programme_trimestre(cls,programme):
        programme_trimestre = cls.objects.filter(programme=programme)
        for i in programme_trimestre:
            return i

# -------------------------------Table Doucument_Fournir----------------------------------------------------
from django.db import models

def chemin_telechargement(instance, filename):
    return f"documents/{instance.pk}/{filename}"

class Document_Fournir(models.Model):
    releve_note = models.FileField(upload_to=chemin_telechargement)
    attestation = models.FileField(upload_to=chemin_telechargement)
    lettre_motivation = models.FileField(upload_to=chemin_telechargement)
    piece_identite = models.FileField(upload_to=chemin_telechargement)
    acte_Naissance = models.FileField(upload_to=chemin_telechargement)

    def pdf_link(self, field_name):
        file_field = getattr(self, field_name)
        if file_field:
            return format_html(
                '<a href="{}" target="_blank">Ouvrir </a>',
                reverse('admin:view_document', args=[self.pk, field_name])
            )
        return 'No PDF available'

    pdf_link.allow_tags = True
    pdf_link.short_description = 'PDF Link'

    def __str__(self):
        return "Documents Fournis"
# -------------------------------Table Coordonne_Bancaire----------------------------------------------------

class Coordonne_Bancaire(models.Model):
    Identifiant = models.CharField("Nom sur la Carte ",max_length=100)
    num_Bancaire = models.CharField("Numéro de banque", max_length=250)
    code_banque = models.CharField("Code Banque",max_length=10)
    date_expiration =models.CharField(max_length=10)
    def __str__(self):
        return self.Identifiant

# -------------------------------Table Paiement----------------------------------------------------

import random
import string

def generate_payment_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
class Paiement(models.Model):
    methode_paiement = models.CharField(max_length=100)
    frais_admission = models.FloatField(max_length=6)
    Coordonne_Bancaire = models.ForeignKey(Coordonne_Bancaire, on_delete=models.CASCADE)
    datelimite=models.DateField()
    numero_paiement=models.CharField(max_length=25)


# -------------------------------Table Demander----------------------------------------------------
from Utilisateurs.models import Utilisateurs
class Demander_Admission(models.Model):
    CHOIX_STATUT = [
        ('accepte', 'Accepté'),
        ('refus', 'Refusé'),
        ('attente', 'En Attente'),
    ]
       
    demandeur = models.OneToOneField(Utilisateurs,on_delete=models.CASCADE)
    date_Soumision = models.DateField()
    ProgrammeTrimestre = models.ForeignKey(ProgrammeTrimestre,on_delete=models.CASCADE)
    Document_Fournir = models.ForeignKey(Document_Fournir,on_delete=models.CASCADE)
    Information_Personnel = models.ForeignKey(Information_Personnelle,on_delete=models.CASCADE)
    Paiement_Admission = models.ForeignKey(Paiement, on_delete=models.CASCADE)
    statut_demande = models.CharField(max_length=10,choices=CHOIX_STATUT,default='attente')
    

    # def __str__(self):
    #     return f"{self.Information_Personnel.nom  }"