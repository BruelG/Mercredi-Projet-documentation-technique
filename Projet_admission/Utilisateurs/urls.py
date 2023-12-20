from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', login_view, name='admission'),
    path('register/', register_user, name="register_user"),
    path('confirmer/',Confirmer_Couriel_view,name='confirmerCourriel'),
    path('accuiel/', pages_accuiel_view, name='accuiel'),
    path('profil/', profil_view, name='profil'),
    path('deconnexion/',deconnexion_view,name='deconnexion'),
    path('modification_profil/',modification_profil_view,name='modification_profil'),
    path('etat_demande/',etat_demande,name='etat_demande'),


]
# urlpatterns = [
#     path('', login_view, name='admission'),
#     path('register/', register_user, name="register_user"),
#     path('accuiel/', pages_accuiel_view, name='accuiel'),
#     path('profil/', profil_view, name='profil'),
#     path('deconnexion/',deconnexion_view,name='deconnexion'),
#     path('modification_profil/',modification_profil_view,name='modification_profil'),

# ]
