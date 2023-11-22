from django.shortcuts import render , redirect

from django.contrib import messages

# Create your views here.

from cours.models import Cours , Cours_Session, Cours_Etudiants

from utilisateur.models import Utilisateur

from comptabilite.models import Facture

import datetime


def index(request):
    if request.method == "GET":
        if str(request.user) != "AnonymousUser":
            utilisateur : Utilisateur = request.user
            """
            On recupere tout les cours de sa session actuelle
            de son cycle actuel
            et de son programme actuel
            """
            cours = Cours_Session.objects.filter(session=utilisateur.session)

            lesCours = []

            for cour in cours :
                leCour = Cours.objects.get(pk=cour.cours.id)
                if(leCour.programme.id == utilisateur.programme.id) and (leCour.cycle.id == utilisateur.cycle.id):
                    lesCours.append(leCour)

            #On recupere sa facture pour son cycle actuel

            facture = Facture.objects.get(etudiant = utilisateur, cycle=utilisateur.cycle)



            return render(request,"dashboard/index.html", {"cours":lesCours,"facture":facture})
        else:
            return redirect("/")
    else :
        return redirect("/")
    
def valider_ajout_cours(request):
    if request.method == "POST":
        if str(request.user) != "AnonymousUser":
            data = request.POST
            cour_id = data.get("cour_id")
            cour = Cours.objects.get(pk=cour_id)
            utilisateur : Utilisateur = request.user

            # On verifie s'il ne fait pas actuellement ce cours dans cette session
            try:
                # Il a ce cours pour cette session
                cour_existant = Cours_Etudiants.objects.get(cours_id=cour_id,etudiant_id=utilisateur.pseudo,session_id=utilisateur.session.id)
                # On verifie si le cours est en cour (entrain d'etre donné actuellement)
                if(cour_existant.credit == -1):
                    # Il suit actuellement ce cours (pas encore fini)
                    messages.error(request,"Vous êtes entrain de suivre ce cours actuellement, Il ne peut pas être ajouté")
                    return redirect('dashboard:index')
                messages.error(request,"Veuillez vous rendre à l'administration")
                return redirect('dashboard:index')

            except Cours_Etudiants.DoesNotExist:
                #Il ne fait pas actuellement le cours dans cette session donc on peut l'ajouter
                cour_session = Cours_Session.objects.get(session=utilisateur.session,cours=cour)

                # On verifie si la date d'ajout depasse la date de debut de 10 jours non ne fais pas l'ajout.
                dateDebut = cour_session.date_debut
                today = datetime.datetime.now().date()
                numberDays = (today -  dateDebut).days
                if (numberDays > 10):
                    messages.error(request,"La date d'ajout est dépassée de 10 jours, vous ne pouvez pas ajouter ce cours. Veuillez aller à l'administration")
                    return redirect('dashboard:index')
                else:
                    # Dans le cas contraire si la date d'ajout n'est pas dépassée

                    #On verifie si ce cours à des prerequis:
                    if(cour.prerequis.count()>0):

                        for prerequis in cour.prerequis.all():
                            try:
                                #On verifie s'il a déjà fait ce cour prerequis en verifiant si une note existe pour lui pour ce cour
                                dejaFait = Cours_Etudiants.objects.get(cours_id=prerequis.id,etudiant_id=utilisateur.pseudo,credit__gt=0)
                            except Cours_Etudiants.DoesNotExist:
                                #Si cela n'existe pas, il ne peut pas faire ce cour car il n'a pas fait ce prerequis
                                messages.error(request,f"Vous ne pouvez pas faire ce cours car il a comme prerequis {prerequis.designation}")
                                return redirect('dashboard:index')
                        
                        # Il n'est pas inscrit à ce cours, pour cette session, on peut l'inscrire.
                        # et il a tout les prerequis
                        nouveauCour = Cours_Etudiants(
                            etudiant = utilisateur,
                            cours = cour,
                            date_inscription = datetime.datetime.now().date(),
                            session = utilisateur.session
                        )
                        nouveauCour.save()
                        messages.success(request,"Le cours a été ajouté avec succes")
                        return redirect('dashboard:index')

                    else:
                        # Il n'est pas inscrit à ce cours, pour cette session, on peut l'inscrire.
                        # et le cour n'a pas de pre-requis
                        nouveauCour = Cours_Etudiants(
                            etudiant = utilisateur,
                            cours = cour,
                            date_inscription = datetime.datetime.now().date(),
                            session = utilisateur.session
                        )
                        nouveauCour.save()
                        messages.success(request,"Le cours a été ajouté avec succes")
                        return redirect('dashboard:index')

            return redirect("dashboard:index")
        else:
            return redirect("/")
    else :
        return redirect("/")
    

def mes_cours(request):
    if request.method == "GET":
        if str(request.user) != "AnonymousUser":
            utilisateur : Utilisateur = request.user
            """
            On recupere tout les cours de sa session actuelle
            de son cycle actuel
            et de son programme actuel
            qu'il fait
            """
            cours = Cours_Etudiants.objects.filter(session=utilisateur.session,etudiant=utilisateur)

            lesCours = []
            dates = []

            for cour in cours :
                leCour = Cours.objects.get(pk=cour.cours.id)
                lesCours.append(leCour)
                coursSession = Cours_Session.objects.get(session = utilisateur.session,cours=leCour)
                dates.append(coursSession.date_ase)


            return render(request,"dashboard/mescours.html", {"cours":cours,"dates":dates})
        else:
            return redirect("/")
    else :
        return redirect("/")
    

def annuler_cours(request):
    if request.method == "POST":
        if str(request.user) != "AnonymousUser":
            utilisateur : Utilisateur = request.user
            data = request.POST
            cours_id = data.get("id_cours")
            
            
            leCour = Cours.objects.get(pk=cours_id)
            coursSession = Cours_Session.objects.get(session = utilisateur.session,cours=leCour)

            dateAujour = datetime.datetime.now().date()

            cours = Cours_Etudiants.objects.get(session=utilisateur.session,etudiant=utilisateur,cours=leCour)

            if(dateAujour > coursSession.date_ase):
                cours.credit = 0
                cours.save()
                messages.success(request,"Le cours a été annulé avec succes mais avec une mention d'echec")
                return redirect('dashboard:mescours')
            else:
                cours.delete()
                messages.success(request,"Le cours a été annulé avec succes")
                return redirect('dashboard:mescours')
        else:
            return redirect("/")
    else :
        return redirect("/")
    

def grille(request):
    if request.method == "GET":
        if str(request.user) != "AnonymousUser":
            utilisateur : Utilisateur = request.user
            """
            On recupere tout les cours de sa
            de son cycle actuel
            et de son programme actuel
            qu'il fait
            """
            cours = Cours.objects.filter(programme=utilisateur.programme,cycle=utilisateur.cycle)

            CoursSES1 = []
            CoursSES2 = []
            CoursSES3 = []
            CoursSES4 = []
            CoursSES5 = []
            CoursSES6 = []

            for cour in cours :
                if(cour.dispenseEn == 1):
                    CoursSES1.append(cour)
                elif(cour.dispenseEn == 2):
                    CoursSES2.append(cour)
                elif(cour.dispenseEn == 3):
                    CoursSES3.append(cour)
                elif(cour.dispenseEn == 4):
                    CoursSES4.append(cour)
                elif(cour.dispenseEn == 5):
                    CoursSES5.append(cour)
                elif(cour.dispenseEn == 6):
                    CoursSES6.append(cour)


            return render(request,"dashboard/grille.html", 
                          {"coursses1":CoursSES1,
                           "coursses2":CoursSES2,
                           "coursses3":CoursSES3,
                           "coursses4":CoursSES4,
                           "coursses5":CoursSES5,
                           "coursses6":CoursSES6
                           }
            )
        else:
            return redirect("/")
    else :
        return redirect("/")
    

def ajouterPlusiersCours(request):
    if request.method == "GET":
        if str(request.user) != "AnonymousUser":
            utilisateur : Utilisateur = request.user
            """
            On recupere tout les cours de sa session actuelle
            de son cycle actuel
            et de son programme actuel
            """
            cours = Cours_Session.objects.filter(session=utilisateur.session)

            lesCours = []

            for cour in cours :
                leCour = Cours.objects.get(pk=cour.cours.id)
                if(leCour.programme.id == utilisateur.programme.id) and (leCour.cycle.id == utilisateur.cycle.id):
                    lesCours.append(leCour)

            return render(request,"dashboard/ajouterplusieurscours.html", {"cours":lesCours})
        else:
            return redirect("/")
    else :
        return redirect("/")
    
def valider_ajout_plusieurs_cours(request):
    if request.method == "POST":
        if str(request.user) != "AnonymousUser":
            data = request.POST
            cour_ids = data.getlist("coursids[]")
            
            for cour_id in cour_ids:
                cour = Cours.objects.get(pk=int(cour_id))
                utilisateur : Utilisateur = request.user

                # On verifie s'il ne fait pas actuellement ce cours dans cette session
                try:
                    # Il a ce cours pour cette session
                    cour_existant = Cours_Etudiants.objects.get(cours_id=cour_id,etudiant_id=utilisateur.pseudo,session_id=utilisateur.session.id)
                    # On verifie si le cours est en cour (entrain d'etre donné actuellement)
                    if(cour_existant.credit == -1):
                        # Il suit actuellement ce cours (pas encore fini)
                        messages.error(request,f"Vous êtes entrain de suivre ce cours actuellement({cour_existant.cours.nom}), Il ne peut pas être ajouté")
                    messages.error(request,f"Veuillez vous rendre à l'administration pour ce cours: {cour_existant.cours.nom}")

                except Cours_Etudiants.DoesNotExist:
                    #Il ne fait pas actuellement le cours dans cette session donc on peut l'ajouter
                    cour_session = Cours_Session.objects.get(session=utilisateur.session,cours=cour)

                    # On verifie si la date d'ajout depasse la date de debut de 10 jours non ne fais pas l'ajout.
                    dateDebut = cour_session.date_debut
                    today = datetime.datetime.now().date()
                    numberDays = (today -  dateDebut).days
                    if (numberDays > 10):
                        messages.error(request,f"La date d'ajout est dépassée de 10 jours pour le cours {cour_session.cours.nom}, vous ne pouvez pas ajouter ce cours. Veuillez aller à l'administration")
                    else:
                        # Dans le cas contraire si la date d'ajout n'est pas dépassée

                        #On verifie si ce cours à des prerequis:
                        if(cour.prerequis.count()>0):

                            for prerequis in cour.prerequis.all():
                                try:
                                    #On verifie s'il a déjà fait ce cour prerequis en verifiant si une note existe pour lui pour ce cour
                                    dejaFait = Cours_Etudiants.objects.get(cours_id=prerequis.id,etudiant_id=utilisateur.pseudo,credit__gt=0)
                                except Cours_Etudiants.DoesNotExist:
                                    #Si cela n'existe pas, il ne peut pas faire ce cour car il n'a pas fait ce prerequis
                                    messages.error(request,f"Vous ne pouvez pas faire ce cours {cour.nom}  car il a comme prerequis {prerequis.designation}")
                            
                            # Il n'est pas inscrit à ce cours, pour cette session, on peut l'inscrire.
                            # et il a tout les prerequis
                            nouveauCour = Cours_Etudiants(
                                etudiant = utilisateur,
                                cours = cour,
                                date_inscription = datetime.datetime.now().date(),
                                session = utilisateur.session
                            )
                            nouveauCour.save()
                            messages.success(request,f"Le cours {cour.nom} a été ajouté avec succes")

                        else:
                            # Il n'est pas inscrit à ce cours, pour cette session, on peut l'inscrire.
                            # et le cour n'a pas de pre-requis
                            nouveauCour = Cours_Etudiants(
                                etudiant = utilisateur,
                                cours = cour,
                                date_inscription = datetime.datetime.now().date(),
                                session = utilisateur.session
                            )
                            nouveauCour.save()
                            messages.success(request,f"Le cours {cour.nom} a été ajouté avec succes")

            return redirect('dashboard:ajouterplusieurscours')
        else:
            return redirect("/")
    else :
        return redirect("/")