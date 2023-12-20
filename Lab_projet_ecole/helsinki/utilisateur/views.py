from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Utilisateur

@api_view(['POST'])
def enregistrer_utilisateur(request):
    if request.method == 'POST':
        # Récupérer les données de la demande POST
        
        pseudo = request.data.get('code_utilisateur')
        mdp = request.data.get('mdp')
        email = request.data.get('email')
       
        # Créer un nouvel utilisateur dans la base de données du projet B
        utilisateur = Utilisateur(
            
            pseudo=pseudo,
            mdp=mdp,
            email=email,
            
        )
        utilisateur.save()

        return Response({'message': 'Utilisateur enregistré avec succès dans le projet B'}, status=status.HTTP_201_CREATED)
