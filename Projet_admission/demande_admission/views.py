import json
import time
from django.shortcuts import render,redirect
from datetime import timedelta
from django.urls import reverse
from Utilisateurs.models import Utilisateurs
from .models import Document_Fournir,Demander_Admission,generate_payment_number,Coordonne_Bancaire, Information_Personnelle, Programme,Trimestre,ProgrammeTrimestre,Paiement
from datetime import datetime
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def initialize_steps(request):
    return {
        'step_1_validated': False,
        'step_1_validated_icon': False,
        'step_2_validated': False,
        'step_2_validated_icon': False,
        'step_3_validated': False,
        'step_3_validated_icon': False,
        'step_4_validated': False,
        'step_4_validated_icon': False,
        'type_admission': request.session.get("type_admission", None)
    }
def base_demande_view(request):
    resul = initialize_steps(request)
    resul['step_1_validated'] = True
    return render(request, 'demande_admission/base_demande.html', context=resul) 
def etape_1_programme(request):  
    if 'type_admission' in request.session:
        type_admission = request.session["type_admission"]
        tout_programme = Programme.get_programmes_by_type_admission(type_admission)
        anne_actulle = datetime.now()
        ann=anne_actulle.year + 1
        trimestre_anne = Trimestre.get_anne_trimest_by_anne(annee=ann)
        context = {
            'programme': tout_programme,
            'Trimestre': trimestre_anne
        }
        erreur = ""
        if request.method == "POST":
            nom_trimestre , annee_trimestre  = request.POST.get("Trimestre").split()
            programme_selection = request.POST.get("programme")
            programme = Programme.objects.filter(titre=programme_selection).first()
            trimestre = Trimestre.objects.filter(nom=nom_trimestre,annee=annee_trimestre).first()
            if programme and trimestre:
                programme_trimestre = ProgrammeTrimestre.get_programme_trimestre(programme)
                # print (f"Voila le programmme : {programme_trimestre}")
                if not programme_trimestre or str(programme_trimestre.trimestre) != request.POST.get("Trimestre"):
                    erreur = "Ce Programme n'est pas disponible pour la trimestre selection"
                    context = {
                        'programme': tout_programme,
                        'Trimestre': trimestre_anne,
                        'Erreur':erreur
                    }
                    return render(request, 'demande_admission/etape_1_programme.html',context=context)
                else:
                    request.session['programme_trimestre_id'] = programme_trimestre.id
                    resul = initialize_steps(request)
                    resul['step_1_validated'] = False
                    resul['step_1_validated_icon'] =True
                    resul['step_2_validated'] = True
                    return render(request, 'demande_admission/base_demande.html', context=resul)
    return render(request, 'demande_admission/etape_1_programme.html', context=context)
def etape_2_information(request):
    if request.method == 'POST':
        nom=request.POST.get("nom")
        prenom=request.POST.get("prenom")
        date_naissance=request.POST.get("date_naissance")
        lieu_naissance=request.POST.get("lieu_naissance")
        adresse=request.POST.get("adresse")
        telephone=request.POST.get("telephone")
        email=request.POST.get("email")
        sexe=request.POST.get("sexe")
        nationalite=request.POST.get("nationalite")
        statut_matrimonial=request.POST.get("status_Matrimoniale")
        role=request.POST.get("role")
        emailExist=Information_Personnelle.objects.filter(email=email)
        frais_admission = 109.0 if nationalite == 'Canadien' else 144.0
        request.session['frais_admission']=frais_admission
        if emailExist:
           erreur = "L'adresse e-mail existe déjà dans notre système. Veuillez utiliser une autre adresse e-mail."
           context={
                'erreur':erreur
            }
           return render(request, 'demande_admission/etape_2_information.html', context=context)
        request.session['Information_Personnelle']={
            'nom':nom,
            'prenom':prenom,
            'date_naissance':date_naissance,
            'lieu_naissance':lieu_naissance,
            'adresse':adresse,
            'telephone':telephone,
            'email':email,
            'sexe':sexe,
            'nationalite':nationalite,
            'status_Matrimoniale':statut_matrimonial,
            'role':role
        }
        resul = initialize_steps(request)
        resul['step_1_validated'] = False
        resul['step_1_validated_icon'] =True
        resul['step_2_validated'] = False
        resul['step_2_validated_icon'] =True
        resul['step_3_validated'] = True
        return render(request, 'demande_admission/base_demande.html', context=resul)
    return render(request, 'demande_admission/etape_2_information.html')
import cv2
import os

def prendre_photo_si_objet_encadre(nom_fichier='photo_capturee.jpg', camera_index=0, largeur=640, hauteur=480):
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la caméra.")
        return None
    
    # Définir la résolution souhaitée
    cap.set(3, largeur)
    cap.set(4, hauteur)
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Erreur lors de la capture de l'image.")
            break

        # Convertir l'image en niveaux de gris pour la détection de visage
        frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Utiliser un détecteur de visage pré-entraîné (haarcascade_frontalface_default.xml)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(frame_gris, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            # Dessiner un rectangle autour du visage détecté
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Si le visage est correctement encadré, prendre la photo
            if w > largeur / 2 and h > hauteur / 2:
                chemin_fichier = os.path.join(os.getcwd(), nom_fichier)
                cv2.imwrite(chemin_fichier, frame)
                print(f"Photo enregistrée sous {chemin_fichier}")

                cap.release()
                return chemin_fichier

        # Afficher le flux vidéo en temps réel avec les rectangles de détection
        cv2.imshow('Camera', frame)

        # Quitter la boucle si la touche 'q' est enfoncée
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
def etape_3_document(request):
    if request.method=="POST":
       # data = json.loads(request.body)
        releve_note=request.FILES['releve_note']
        attestation_note=request.FILES['attestation']
        lettre_note=request.FILES['lettre_motivation']
        piece_note=request.FILES['piece_identite']
        acte=request.FILES['acte_Naissance']
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_documents')
        os.makedirs(temp_dir, exist_ok=True)
        def save_file(file, file_name):
                file_path = os.path.join(temp_dir, file_name)
                with default_storage.open(file_path, 'wb+') as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                return file_path
        releve_note_path = save_file(releve_note, releve_note.name)
        attestation_note_path = save_file(attestation_note, attestation_note.name)
        lettre_note_path = save_file(lettre_note, lettre_note.name)
        piece_note_path = save_file(piece_note, piece_note.name)
        acte_path = save_file(acte, acte.name)
        request.session['documents'] = {
            'releve_note': releve_note_path,
            'attestation': attestation_note_path,
            'lettre_motivation': lettre_note_path,
            'piece_identite': piece_note_path,
            'acte_Naissance': acte_path,
        }
        resul = initialize_steps(request)
        resul['step_1_validated'] = False
        resul['step_1_validated_icon'] =True
        resul['step_2_validated'] = False
        resul['step_2_validated_icon'] =True
        resul['step_3_validated'] = False
        resul['step_3_validated_icon'] =True
        resul['step_4_validated'] = True
        return render(request, 'demande_admission/base_demande.html', context=resul)
    type_admission = request.session["type_admission"]
    ctx = {
        "type_admission": type_admission,
    }
    return render(request, 'demande_admission/etape_3_document.html',context=ctx)
def etape_4_payer(request):
    frais_admission = request.session.get('frais_admission')
    if request.method == "POST":
        request.session ["mode_paiement"] = "visa_card"
        nom_carte = request.POST.get("nom_carte")
        num_carte = request.POST.get("num_carte")
        date_expiration = request.POST.get("date_expiration")
        cvv = request.POST.get("cvv")
        request.session ["Coordonne_Bancaire"] = {
            "Identifiant": nom_carte,
            "num_Bancaire": num_carte,
            "date_expiration": date_expiration,
            "code_banque": cvv
        }
        resul = initialize_steps(request)
        resul['step_1_validated'] = False
        resul['step_1_validated_icon'] =True
        resul['step_2_validated'] = False
        resul['step_2_validated_icon'] =True
        resul['step_3_validated'] = False
        resul['step_3_validated_icon'] =True
        resul['step_4_validated'] = False
        resul['step_4_validated_icon'] =True
        resul['step_5_validated'] = True
        return render(request, 'demande_admission/base_demande.html', context=resul)
    context = {
        "frais_admission":frais_admission
    }
    return render(request, 'demande_admission/etape_4_paiement.html',context=context)
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
def send_confirmation_email(email, information_personnelle):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'anonymousteccart@gmail.com'
    sender_password = 'ddnh pgpe yape wchg'
    message = MIMEText(
        f"""
        <html>
            <head>
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        background-color: #f6f6f6;
                        padding: 20px;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 0 auto;
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 5px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }}
                    h2 {{
                        color: #007bff;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h2>Confirmation de la demande d'admission en ligne à l'UQAM</h2>
                    <p>Bonjour {information_personnelle['prenom']} {information_personnelle['nom']},</p>
                    <p>Nous vous confirmons la réception de votre demande d'admission en ligne à l'UQAM. Votre demande est actuellement en attente de traitement. Nous vous informerons dès qu'il y aura des mises à jour.</p>
                    <p>Merci de votre intérêt envers l'UQAM.</p>
                    <p>Cordialement,<br>L'équipe d'Admission UQAM</p>
                </div>
            </body>
        </html>
        """, "html"
    )
    
    message["Subject"] = "Confirmation de la demande d'admission à l'UQAM"
    message["From"] = sender_email
    message["To"] = email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())

def etape_5_confirmer(request):
    programme_trimestre = request.session.get('programme_trimestre', {})
    information_personnelle = request.session.get('Information_Personnelle', {})
    type_demande = request.session.get('type_admission')
    trimestreProg_id = request.session.get('programme_trimestre_id')
    # Définissez la variable context en dehors de la condition POST
    context = {
        'programme_trimestre': programme_trimestre,
        'information_personnelle': information_personnelle,
        'type_admissin': type_demande
    }
    cod_user = request.session.get('user_id')
    user,sucess = Utilisateurs.get_user_id(cod_user)
    user = user.get("code_user")
    if sucess:
      user_instance = Utilisateurs.objects.filter(code_user=user).first()
    if request.method == "POST":
        # Assurez-vous que trimestreProg_id est un entier
        if isinstance(trimestreProg_id, int):
            # Utilisez trimestreProg_id pour récupérer les instances nécessaires de ProgrammeTrimestre, Programme, et Trimestre
            programme_trimestre_instance = ProgrammeTrimestre.objects.get(id=trimestreProg_id)
            programme_instance = programme_trimestre_instance.programme
            trimestre_instance = programme_trimestre_instance.trimestre

            # Reste du code...
            existing_demande = Demander_Admission.objects.filter(demandeur=user_instance).first()
            if existing_demande:
                # Si une demande existe déjà, gérez la situation en conséquence
                context['error'] = 'Vous avez déjà soumis une demande d\'admission.'
                return render(request, 'demande_admission/etape_5_confirmer.html', context=context)

            # Enregistrez les informations de la demande dans la base de données
            date_limite = datetime.now() + timedelta(days=7)
            numero_paiement = generate_payment_number()
            coordonnee_bancaire_data = request.session.get('Coordonne_Bancaire')
            coordonnee_bancaire = Coordonne_Bancaire.objects.create(**coordonnee_bancaire_data)
            cod_user = request.session.get('user_id')
            user, sucess = Utilisateurs.get_user_id(cod_user)
            user_instance = user_instance
            documents = request.session.get('documents')
            # Validation des données avant l'enregistrement
            demande_admission = Demander_Admission.objects.create(
                demandeur=user_instance,
                date_Soumision=datetime.now(),
                ProgrammeTrimestre=programme_trimestre_instance,
                Document_Fournir=Document_Fournir.objects.create(**documents),
                Information_Personnel=Information_Personnelle.objects.create(**information_personnelle),
                Paiement_Admission=Paiement.objects.create(methode_paiement=request.session.get('mode_paiement'),
                                                           frais_admission=request.session.get('frais_admission'),
                                                           Coordonne_Bancaire=coordonnee_bancaire, datelimite=date_limite,
                                                           numero_paiement=numero_paiement),
                statut_demande='attente'
            )
            if not demande_admission:
                context['error'] = 'Erreur lors de l\'enregistrement de votre demande d\'admission.'
                return render(request, 'demande_admission/etape_5_confirmer.html', context=context)
            if demande_admission.pk:
                email = information_personnelle.get("email")
                send_confirmation_email(email, information_personnelle)
                time.sleep(3)
                return redirect("accuiel")
        else:
            context['error'] = "Erreur: trimestreProg_id n'est pas un entier."
            print("Erreur: trimestreProg_id n'est pas un entier.")
    return render(request, 'demande_admission/etape_5_confirmer.html', context=context)
















# def etape_5_confirmer(request):
#     programme_trimestre = request.session.get('programme_trimestre', {})
#     information_personnelle = request.session.get('Information_Personnelle', {})
#     type_demande = request.session.get('type_admission')
#     trimestreProg_id = request.session.get('programme_trimestre_id')
#     print(f"voila le Programme ID : {trimestreProg_id}")
#     # cod_user = request.session.get('user_id')
#     # user,sucess = Utilisateurs.get_user_id(cod_user)
#     # user = user.get("code_user")
#     # user_instance = Utilisateurs.objects.get(code_user=user)
#     # programme_instance, created_programme = Programme.objects.get_or_create(
#     #         titre=trimestreProg['programme']['titre'],
#     #         type_admission=trimestreProg['programme']['type_admission']
#     #     )
#     # trimestre_instance, created_trimestre = Trimestre.objects.get_or_create(
#     #         nom=trimestreProg['trimestre']['nom'],
#     #         annee=trimestreProg['trimestre']['annee']
#     #     )
#     #   # Recherchez ou créez programme_trimestre_instance en fonction de programme_instance et trimestre_instance
#     # programme_trimestre_instance, created_programme_trimestre = ProgrammeTrimestre.objects.get_or_create(
#     #         programme=programme_instance,
#     #         trimestre=trimestre_instance
#     #     )
#     # # print(f"voila le Programme : {programme_instance}")
#     # # print(f"voila tout  : {programme_trimestre_instance}")
#     # documents = request.session.get('documents')
#     # context = {
#     #     'programme_trimestre': programme_trimestre,
#     #     'information_personnelle': information_personnelle,
#     #     'type_admissin': type_demande
#     # }
#     if request.method == "POST":
#         existing_demande = Demander_Admission.objects.filter(demandeur=user_instance).first()
#         if existing_demande:
#         # If a demande already exists, handle the situation accordingly
#            context = {
#             'programme_trimestre': programme_trimestre,
#             'information_personnelle': information_personnelle,
#             'type_admissin': type_demande,
#             'error': 'Vous avez déjà soumis une demande d\'admission.'
#            }
#            return render(request, 'demande_admission/etape_5_confirmer.html', context=context)
#         # on enregistre les informations de la demande dans la base de données
#         date_limite = datetime.now() + timedelta(days=7)
#         numero_paiement = generate_payment_number()
#         coordonnee_bancaire_data= request.session.get('Coordonne_Bancaire')
#         coordonnee_bancaire = Coordonne_Bancaire.objects.create(**coordonnee_bancaire_data)
#         # Validation des données avant l'enregistrement
#         demande_admission = Demander_Admission.objects.create(
#             demandeur=user_instance,
#             date_Soumision=datetime.now(),
#             ProgrammeTrimestre=programme_trimestre_instance,
#             Document_Fournir=Document_Fournir.objects.create(**documents),
#             Information_Personnel=Information_Personnelle.objects.create(**information_personnelle),
#             Paiement_Admission=Paiement.objects.create(methode_paiement=request.session.get('mode_paiement'),frais_admission=request.session.get('frais_admission'),
#                                                      Coordonne_Bancaire=coordonnee_bancaire, datelimite = date_limite,numero_paiement=numero_paiement),
#             statut_demande='attente'                                         
#             )
#         if not demande_admission:
#             context = {
#             'programme_trimestre': programme_trimestre,
#             'information_personnelle': information_personnelle,
#             'type_admissin': type_demande,
#             'error':'Erreur lors de l\'enregistrement de votre demande d\'admission.'
#         }
#             return render(request, 'demande_admission/etape_5_confirmer.html', context=context)
#         if demande_admission.pk:
#           email = information_personnelle.get("email")
#           send_confirmation_email(email, information_personnelle)
#           time.sleep(3) 
#           return redirect("accuiel")
#     return render(request, 'demande_admission/etape_5_confirmer.html', context=context)


def details_confirmation(request):
    return render(request, 'demande_admission/details_confirmation.html')
