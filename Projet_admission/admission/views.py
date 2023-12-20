from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
 
# pip install openai streamlit streamlit-chat
import openai
openai.api_key = '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'
 
def generate_response(user_input):
    completions = openai.Completion.create(
        engine='text-davinci-003',
        prompt=user_input,
        max_tokens = 1024,
        n=1, 
        stop = None,
        temperature = 0.5,
    )
    message = completions.choices[0].text.strip()
    return message



 
def index_view(request):
    if request.method=='POST':
        message=request.POST.get('message','input')
        response=generate_response(message)
        return JsonResponse({'message':message,'response':response})
    return render(request, 'index.html')
def programme_view(request):

    return render(request, 'programme.html')


def admission_view(request):
    return render(request, 'admissions.html')


def propos_view(request):
    return render(request, 'propos.html')


def contact_view(request):
    return render(request, 'contact.html')


# def send_email():
#     import smtplib
#     import re

# def validate_email(email):
#     # La fonction de validation d'adresse e-mail
#     return re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)

# def send_email(subject, body, from_email, to_email, password):
#     # Vérifier si l'adresse e-mail de destination est valide
#     if not validate_email(to_email):
#         print("Adresse e-mail invalide.")
#         return

#     # Configuration du serveur SMTP
#     smtp_server = "smtp.example.com"  # Remplacez par votre serveur SMTP
#     port = 587  # Port SMTP (peut varier en fonction du fournisseur de messagerie)

#     # Établir une connexion SMTP
#     server = smtplib.SMTP(smtp_server, port)
#     server.starttls()

#     try:
#         # Authentification avec le serveur SMTP
#         server.login(from_email, password)

#         # Créer le message
#         message = f"Subject: {subject}\n\n{body}"

#         # Envoyer l'e-mail
#         server.sendmail(from_email, to_email, message)
#         print("E-mail envoyé avec succès.")
#     except Exception as e:
#         print(f"Une erreur s'est produite: {e}")
#     finally:
#         server.quit()

# # Exemple d'utilisation
# subject = "Sujet de l'e-mail"
# body = "Corps de l'e-mail"
# from_email = "votreadresse@example.com"
# to_email = "destinataire@example.com"
# password = "votremotdepasse"

# send_email(subject, body, from_email, to_email, password)
