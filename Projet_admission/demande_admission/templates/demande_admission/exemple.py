# def etape_5_demande(request):
#     # Récupérer les fichiers de la session
#     documents = request.session.get('documents', None)

#     if documents:
#         # Créer la demande complète avec les informations de la session
#         # Vous devrez adapter cela en fonction de votre modèle Demander_Admission
#         demande = Demander_Admission.objects.create(
#             demandeur=request.user,  # Assurez-vous d'avoir un utilisateur connecté
#             date_Soumision=datetime.now(),
#             ProgrammeTrimestre=request.session['programme_trimestre'],
#             Document_Fournir=Document_Fournir.objects.create(**documents),
#             Information_Personnel=Information_Personnelle.objects.create(**request.session.get('info', {})),
#             Paiement_Admission=Paiement.objects.create(methode_paiement='exemple', frais_admission=100.0, numero_paiement='123456'),
#             statut_demande='attente',
#         )

#         # Nettoyer la session après avoir créé la demande
#         del request.session['documents']
#         del request.session['programme_trimestre']
#         del request.session['info']

#         return render(request, 'demande_admission/etape_5_demande.html', {'demande': demande})


# <div class="container">
#   <img src="{% static 'images/uqam_logo.png' %}" alt="UQAM Logo" class="uqam-logo">
#   <center><h1>Confirmation de demande d'admission à l'UQAM</h1></center>
#   <p>Bonjour,{% if Information_Personnelle.sexe == "Homme" %} Mr {{ Information_Personnelle.nom }}{% else %} Mlle {{ Information_Personnelle.nom }}{% endif %} </p>
#   <p>Nous sommes ravis de vous informer que votre demande d'admission à l'Université du Québec à Montréal (UQAM) a bien été reçue.</p>
#   <p>Programme sélectionné : {{ programme_trimestre.programme.titre }}</p>
#   <p>Trimestre sélectionné : {{ programme_trimestre.trimestre.nom }} {{ programme_trimestre.trimestre.annee }}</p>
#   <p>
#     Veuillez prendre note que cette lettre de confirmation ne constitue pas une acceptation officielle. Vous recevrez une notification officielle dès que votre demande aura été examinée.
#   </p>
#   <div class="text-center mt-4">
#     <a href="{% url 'etape_5' %}" class="btn btn-success">Confirmer la demande</a>
#   </div>
#   <p>Merci de choisir l'UQAM pour poursuivre vos études supérieures. Nous sommes impatients de vous accueillir sur notre campus.</p>
#   <p>Cordialement,</p>
#   <p>L'Équipe d'Admission<br>Université du Québec à Montréal</p>
# </div>