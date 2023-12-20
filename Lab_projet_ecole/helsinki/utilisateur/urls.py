from django.urls import path
from . import views

urlpatterns = [
    path('api/enregistrer_utilisateur/', views.enregistrer_utilisateur, name='enregistrer_utilisateur'),
    
]
