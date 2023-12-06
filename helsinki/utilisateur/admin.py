from django.contrib import admin

from .models import Utilisateur , UtilisateurSession

# Register your models here.


admin.site.register([Utilisateur,UtilisateurSession])
