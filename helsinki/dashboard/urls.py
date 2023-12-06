"""
URL configuration for helsinki project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include

from .views import *

app_name = "dashboard"


urlpatterns = [
    path("",index, name="index"),
    path("valider-ajout/",valider_ajout_cours,name="validerajoutcour"),
    path("mes-cours/",mes_cours, name="mescours"),
    path("annuler-cours/",annuler_cours,name="annulercours"),
    path("grille-de-cheminement/",grille,name="grilledecheminement"),
    path("ajouter-plusieurs-cours/",ajouterPlusiersCours,name="ajouterplusieurscours"),
    path("valider-ajout-plusieurs-cours/",valider_ajout_plusieurs_cours,name="validerajoutplusieurscour"),
]
