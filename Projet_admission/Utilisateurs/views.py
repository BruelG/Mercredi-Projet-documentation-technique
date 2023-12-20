from django.conf import settings
from email.message import EmailMessage
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.shortcuts import render, redirect
# from .Class import Comptes
from .models import Utilisateurs
import random
from demande_admission.models import Programme
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import requests

def send_confirmation_email(email, Nom_user):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'anonymousteccart@gmail.com'
    sender_password = 'ddnh pgpe yape wchg'
    code_6 = ''.join(str(random.randint(0, 9)) for _ in range(6))

    message = MIMEMultipart("alternative")
    message["Subject"] = 'Confirmation: ouverture d\'un compte d\'Admission en ligne à l\'UQAM'
    message["From"] = sender_email
    message["To"] = email

    html = f"""\
    <html>
      <head></head>
      <body>
        <div style="font-family: Arial, sans-serif; background-color: #f6f6f6; padding: 20px;">
          <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #007bff;">Confirmation: ouverture d'un compte d'Admission en ligne à l'UQAM</h2>
            <p>Bonjour, {Nom_user},</p>
            <p>Nous vous confirmons la création de votre compte d'admission en ligne de l'UQAM. Vous pouvez utiliser le code suivant pour finaliser votre inscription : <strong>{code_6}</strong>.</p>
            <p>Ce compte vous permettra de soumettre et de visualiser vos demandes d'admission à notre institution et de prendre connaissance des décisions prononcées.</p>
            <p>Nous vous remercions de votre intérêt envers l'UQAM et vous prions d'agréer nos salutations les plus cordiales.</p>
            <p>L'équipe de l'Admission.</p>
            <p>Note : Ne répondez pas à ce courriel. Celui-ci est généré automatiquement. Pour toute question, visitez le site : <a href="#" style="color: #007bff;">UQAM</a></p>
          </div>
        </div>
      </body>
    </html>
    """

    part = MIMEText(html, "html")
    message.attach(part)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())
    return code_6




def login_view(request):
    response = ''
    if request.method == 'POST':
        code_user = request.POST.get('code_user')
        password = request.POST.get('password')
        user, success = Utilisateurs.login_user(code_user=code_user, password=password)
        if success:
            request.session['user_id'] = user.get('id')
           # response.set_cookie('code_user', code_user)
            response= redirect('accuiel')
            return response
        else:
           context =  {"error_message" : 'Code utilisateur ou mot de passe incorrect. Veuillez réessayer.'}
           return render(request, 'Utilisateurs/login.html', context=context)
    return render(request, 'Utilisateurs/login.html')

def register_user(request):
    if request.method == "POST":
        code_user = request.POST.get('code_user')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            existing_code_user = Utilisateurs.objects.filter(code_user=code_user).first()
            if not existing_code_user is None:
                context =  {"error_message" : 'Code utilisateur exist.Veuillez réessayer.'}
                return render(request, 'Utilisateurs/registre.html', context=context)
            request.session['code_user'] = code_user
            request.session['password'] = password
            request.session['email'] = email
            code = send_confirmation_email(email, code_user)
            request.session['code_6'] = code
           
            return redirect("confirmerCourriel")
        except Exception as e:
            context =  {"error_message" : e}
            return render(request, 'Utilisateurs/registre.html', context=context)
    return render(request, 'Utilisateurs/registre.html')
        
def Confirmer_Couriel_view(request):
     if request.method == "POST":
            code_user = request.POST.get('code_confirmation')
            code = request.session.get('code_6')
            code_user_saved = request.session.get('code_user')
            password = request.session.get('password')
            email = request.session.get('email')
            
            if code_user == code:
                new_user = Utilisateurs.objects.create(code_user=code_user_saved, password=password, email=email, actifs=True)
                new_user.save()
                del request.session['code_6']
                del request.session['password']
                del request.session['email']

        

                return redirect("admission")
            else:
                error_message= 'Code utilisateur invalide. Veuillez réessayer.'
                return render(request, 'Utilisateurs/confirme_Courriel.html', {'error_message': error_message})
     return render(request, 'Utilisateurs/confirme_Courriel.html')
from demande_admission.models import Demander_Admission
def pages_accuiel_view(request):
    id_user = request.session['user_id']
    info_user,success = Utilisateurs.get_user_id(id_user)
    if success:
        user,success = Utilisateurs.get_user_id(id_user)
        user = user.get("code_user")
        user_instance = Utilisateurs.objects.get(code_user=user)
        demande_admission = Demander_Admission.objects.filter(demandeur=user_instance).first()
        #print(demande_admission)
        types_admission = Programme.get_all_type_admission()
        context = {
            'info_user' : info_user,
            'types_admission' : types_admission,
            'demande_admission' : demande_admission
        }
        if request.method == 'POST':
            type_admission = request.POST.get('type')
            request.session['type_admission'] = type_admission
            return redirect("base_demande")
        return render(request,'Utilisateurs/accueil.html',context=context)
    return render(request, 'Utilisateurs/accueil.html')


def profil_view(request):
    id_user = request.session['user_id']
    info_user,success = Utilisateurs.get_user_id(id_user)
    if success:
        context = {
            'info_user' : info_user,
        }
        return render(request,'Utilisateurs/accueil.html',context=context)
    return render(request, 'Utilisateurs/profil.html')
def deconnexion_view(request):
    del request.session['user_id']
    return redirect('admission')

def modification_profil_view(request):
    return render(request, 'Utilisateurs/modification_profil.html');
import cv2
import pytesseract
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
def etat_demande(request):
    id_user = request.session['user_id']
    user,success = Utilisateurs.get_user_id(id_user)
    user = user.get("code_user")
    user_instance = Utilisateurs.objects.get(code_user=user)
    demande_admission = Demander_Admission.objects.filter(demandeur=user_instance).first()
    context = {
        'demande_admission' : demande_admission
    }
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\KASSAMBARA ABRAMANE\source\repos\My_Projet\Projet_Admission\prj_Admission_DT\Tesseract-OCR\tesseract.exe'
    documents = demande_admission.Document_Fournir
    releve_note = documents.releve_note
    atesttation = documents.attestation
    acte_naissance = documents.acte_Naissance
    lettre_motivation = documents.lettre_motivation
    piece_identite = documents.piece_identite
    print(f"voila releve : {releve_note}")
    print(f"voila attesation : {atesttation}")
    print(f"voila acte naissance : {acte_naissance}")
    print(f"voila lettre motivation : {lettre_motivation}")
    print(f"voila pience identite : {piece_identite}")
    def extract_text_from_image(image_path):
        image = cv2.imread(str(image_path))
        if image is None:
          return print(f"Voila de l'image échouée : {image_path}")
        else:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            resized_image = cv2.resize(gray_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            text = pytesseract.image_to_string(resized_image)
            text = pytesseract.image_to_string(gray_image)
            if text.strip() == "":
                print(f"Tesseract n'a pas pu extraire de texte de l'image : {image_path}")
            else:
                print(f"Texte extrait : {text}")
            return text
        #print(f'Chemin de l\'image : {releve_note}')
    text_releve_note = extract_text_from_image(atesttation)
    print(f'Text Releve Note : {text_releve_note}')
    return render(request,'Utilisateurs/etat_demande.html',context=context)