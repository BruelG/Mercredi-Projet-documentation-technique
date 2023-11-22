from django.shortcuts import render , redirect

from django.contrib.auth import authenticate , login , logout

from utilisateur.models import Utilisateur, UtilisateurSession

# Create your views here.

def check_utilisateur(request):
    if request.method == "POST":
        data = request.POST
        pseudo = data.get("pseudo")
        mdp = data.get("mdp")


        user = authenticate(username=pseudo,password=mdp)
        if user is None : 
            print("tata")
            return redirect("/")
        else : 
            usersession = UtilisateurSession.objects.get(user=user)
            print("toto")
            login(request,usersession,backend="utilisateur.backends.UtilisateurBackend")
            return redirect("/dashboard/")
    else:
        return redirect("/")
    


def deconnexion(request):
    logout(request)
    return redirect("/")
