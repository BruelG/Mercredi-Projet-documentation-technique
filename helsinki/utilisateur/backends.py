from django.contrib.auth.backends import ModelBackend

from .models import Utilisateur , UtilisateurSession

class UtilisateurBackend(ModelBackend):
    def authenticate(self,request,**kwargs):
        pseudo = kwargs["username"]
        mdp = kwargs["password"]
        
        try:
            user = Utilisateur.objects.get(pseudo=pseudo,mdp=mdp)
            if user is not None:
                return user
        except Utilisateur.DoesNotExist:
            return None
        
    def get_user(self, pseudo):
        try:
            user = UtilisateurSession.objects.get(pk=pseudo)
            if user is not None:
                return user.user
        except UtilisateurSession.DoesNotExist:
            return None