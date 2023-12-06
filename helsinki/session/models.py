from django.db import models

# Create your models here.

class Session(models.Model):
    nom = models.CharField(max_length=255)


    def __str__(self) -> str:
        return "ID : " + str(self.id) + " - " + self.nom