# Admission.py
from Utilisateurs.models import Utilisateurs
from .models import Demander_Admission
from .traitement import traiter_documents

class Admission:
    @classmethod
    def traiter_demande(cls, demande_id):
        try:
            demande = Demander_Admission.objects.get(pk=demande_id)
            traiter_documents(demande)
        except Demander_Admission.DoesNotExist:
            print(f"La demande avec l'ID {demande_id} n'existe pas.")
