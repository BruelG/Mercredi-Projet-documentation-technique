from django.db import models

# Create your models here.

class Programme(models.Model):
    nom_programme = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.nom_programme
