import streamlit as st
from contribution.contribution_functions import submit_contribution, submit_contribution_author, submit_additional_authors, g_main_topics,show_submitted_informations
#from save_data.save_data_functions import save_contribution_data, show_submitted_information
from confirmation_email.email_functions import send_confirmation_email
# from contribution.modify import modify_information
from camera import process_pdf_analysis
from save_data.save_data_functions import save_contribution_data_snowflake
from contribution.registration_functions import save_payment_info, save_registration_info, confirm_email,save_to_database
import re
import paypalrestsdk
import snowflake.connector
from snowflake.connector import connect, Error
from camera import connect_to_snowflake, insert_pdf_into_snowflake
import snowflake.connector
import base64
from io import BytesIO
import PyPDF2
import pandas as pd
import snowflake.connector
import streamlit as st
from myopenai import mykey
import openai
import time
from googletrans import Translator
from ia import pdf_to_text, fetch_snowflake_data
from camera import select_pdf_file, calculer_pourcentage_lisibilite, calculer_similarite_semantique
from textstat import coleman_liau_index
import PyPDF2  # Ajoutez cette ligne pour l'importation de PyPDF2

# Ajoutez le chargement du modèle spaCy
import spacy
nlp = spacy.load("fr_core_news_sm")

main_topics = ["Academic Publish 2023 :Cloud", "Academic Publish 2023 :Data", "Academic Publish 2023 :Energy",
               "Academic Publish 2023 :Health", "Academic Publish 2023 :Human-Machine", "Academic Publish 2023 :Intelligence",
               "Academic Publish 2023 :Internet", "Academic Publish 2023 :IoT", "Academic Publish 2023 :Learning",
               "Academic Publish 2023 :Meta verse", "Academic Publish 2023 :Mobility", "Academic Publish 2023 :Multimedia"]

def calculate_total_price(selected_registration, extra_pages, extra_gala_dinners):
    # Logique pour calculer le prix total en fonction des options sélectionnées
    # Remplacez cela par votre propre logique
    base_price = 54.00  # Prix de base de l'article scientifique
    extra_pages_price = extra_pages * 105.00
    extra_gala_dinners_price = extra_gala_dinners * 95.00

    total_price = base_price + extra_pages_price + extra_gala_dinners_price
    return total_price
#SUMMARY AND TRANSLATION IA:
# Define your functions here

def connect_to_snowflake():
    return snowflake.connector.connect(
        user='christiane',
        password='Kkcv2002@gkmm',
        account='rwwrqgg-fb48745',
        warehouse='COMPUTE_WH',
        database='RCWPROJET',
        schema='CHRISTIANE'
    )

def fetch_snowflake_data(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM RCWPROJET.CHRISTIANE.CAMERAREADY")
    rows = cur.fetchall()
    cur.close()
    return rows

def process_snowflake_data(rows):
    data = [list(x) for x in rows]
    columns = [desc[0] for desc in cur.description]
    df = pd.DataFrame(data, columns=columns)
    return df

# Connexion à Snowflake
ctx = snowflake.connector.connect(
    user='christiane',
    password='Kkcv2002@gkmm',
    account='rwwrqgg-fb48745',
    warehouse='COMPUTE_WH',
    database='RCWPROJET',
    schema='CHRISTIANE'
)

# Récupérez les informations depuis la table Snowflake
cur = ctx.cursor()
cur.execute("SELECT * FROM RCWPROJET.CHRISTIANE.CAMERAREADY")
rows = cur.fetchall()

def generate_summary(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{text}\n\nGenerate a brief summary of the article:",
            max_tokens=50,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extract the text from the summary response JSON
        summary_text = response['choices'][0]['text'].strip() if response and response['choices'] else None

        return summary_text
    except openai.error.RateLimitError as e:
        st.warning(f"Waiting.... ")
        time.sleep(20)
        return generate_summary(text)
    
def translate_text(text, dest_language):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    except Exception as e:
        return f"Erreur de traduction: {e}"
    
def show_articles():
    # Connexion à Snowflake
    conn = connect_to_snowflake()

    # Récupérez les informations depuis la table Snowflake
    rows = fetch_snowflake_data(conn)

    # Définir la clé OpenAI
    openai.api_key = mykey

    # Convertir les résultats en un DataFrame pandas
    data = [list(x) for x in rows]
    columns = [desc[0] for desc in cur.description]
    df = pd.DataFrame(data, columns=columns)

    # Configuration de la page
    st.title('READ SCIENTIFIC ARTICLES')

    # Transformez le contenu binaire PDF en texte
    df['PDF_CONTENT_TEXT'] = df['PDF_CONTENT_BINARY'].apply(lambda x: pdf_to_text(x))

    # Créer une liste de sujets uniques
    unique_topics = list(set(df['ARTICLE_TOPIC']))

    # Ajouter l'option "Tous les sujets" à la liste de sujets
    unique_topics.insert(0, "Tous les sujets")

    # Sélection de sujet avec une liste déroulante
    selected_topic = st.selectbox("Select the topic:", unique_topics)

    # Filtrer les articles en fonction du sujet sélectionné
    if selected_topic == "Tous les sujets":
        selected_articles = df[['YOUR_FULL_NAME', 'ARTICLE_TITLE', 'PDF_CONTENT_TEXT']]
    else:
        selected_articles = df[df['ARTICLE_TOPIC'] == selected_topic][['YOUR_FULL_NAME', 'ARTICLE_TITLE', 'PDF_CONTENT_TEXT']]

    selected_article_info = st.selectbox('Select the article:', selected_articles.itertuples(index=False), format_func=lambda x: f"{x[0]}, {x[1]}")

    # Display selected article information in columns
    st.header("Selected Article Informations")

    # Display author and title in the first column
    col1, col2 = st.columns([1, 2])
    col1.subheader("Author")
    col1.write(selected_article_info[0])
    col1.subheader("Article Title")
    col1.write(selected_article_info[1])
    summary = generate_summary(selected_article_info[2])
    st.subheader(f"A SUMMARY GERERATED BY IA : ")
    st.write(f'{summary}')

    languages = {"Anglais": "en","Arabe": "ar", "Français": "fr", "Espagnol": "es"}
    selected_language = st.selectbox("Traduire en :", list(languages.keys()))

    # Button for reading the article
    if st.button("Read the Article"):
        # Display PDF content in the second column
        translated_text = translate_text(selected_article_info[2], languages[selected_language])
        st.text_area("Article Traduit", value=translated_text, height=500)

    # Optionally, you can include a button to generate and display the summary

    # Close Snowflake connection
    conn.close()






# Fonction pour la page Camera Ready
def show_CR_page():
    # Connexion à Snowflake
    conn = connect_to_snowflake()
    cursor = conn.cursor()
    

    # Titre de la page
    st.title("Camera Ready - Étapes du processus")

    # ... Code pour les étapes 1 à 6 ...
        
# Étape 1: Paper registration
    st.header("Étape 1: Enregistrement de l'article")
    st.write("Remplissez le formulaire d'enregistrement et soumettez-le comme indiqué dans l'e-mail de notification que vous avez reçu de IARIA.")
    if st.button("Passer à l'Étape 2"):
        st.success("Étape 1 complétée.")

# Étape 2: Deadlines
    st.header("Étape 2: Délais")
    st.write("Les manuscrits finaux (camera ready) feront l'objet d'une révision technique et scientifique finale. Respectez la date limite de soumission des manuscrits.")
    if st.button("Passer à l'Étape 3"):
        st.success("Étape 2 complétée.")

# Étape 3: Content
    st.header("Étape 3: Contenu")
    st.write("Les évaluateurs ont consacré du temps à vous fournir des commentaires. Il est obligatoire de prendre en compte leurs commentaires pour le manuscrit final. Une validation croisée sera effectuée sur la version camera-ready que vous téléchargez à l'étape 7.")
    st.write("Le manuscrit final doit contenir le même contenu que la soumission originale acceptée pour la publication. L'ajout ou la suppression de matériel substantiel n'est pas accepté à cette dernière étape, sauf les modifications requises par les examinateurs.")
    st.write("Pour toute question, veuillez contacter steve@iaria.org qui coordonnera entre les auteurs et le comité technique pour répondre à vos questions.")
    st.write("Il y a un maximum de 6 pages pour une soumission régulière.")
    st.write("Pages supplémentaires : Jusqu'à 4 pages supplémentaires moyennant des frais supplémentaires (soit un total de 10). Voir le formulaire d'inscription pour plus de détails.")
    if st.button("Passer à l'Étape 4"):
        st.success("Étape 3 complétée.")

# Étape 4: Formatting
    st.header("Étape 4: Formatage")
    st.write("Les utilisateurs de MS Word peuvent utiliser ce modèle de page.")
    st.write("Les utilisateurs de Latex peuvent utiliser ces macros.")
    if st.button("Passer à l'Étape 5"):
        st.success("Étape 4 complétée.")

# Étape 5: Producing the PDF
    st.header("Étape 5: Production du PDF")
    st.write("Les utilisateurs de MS Word devront convertir leur travail en PDF pour la soumission du document final. Vous pouvez utiliser un logiciel de bureau pour cette conversion, ou l'un des nombreux services de conversion en ligne gratuits. Une fois la conversion effectuée, veuillez effectuer une vérification finale sur le fichier PDF produit pour vous assurer qu'il reflète correctement votre travail original.")
    st.write("Le fichier PDF que vous soumettez doit avoir les paramètres de sécurité et de restriction suivants : pas de chiffrement par mot de passe, autorisation d'impression, autorisation de copie de contenu et autorisation d'extraction de pages. Les polices doivent être incorporées.")
    if st.button("Passer à l'Étape 6"):
        st.success("Étape 5 complétée.")

# Étape 6: Copyright release
    st.header("Étape 6: Cession de droits d'auteur")
    st.write("Le formulaire de cession de droits d'auteur doit être complété dans le cadre de votre soumission camera ready. En essence, la cession de droits d'auteur est un transfert des droits de publication, qui permet à IARIA et à ses partenaires de promouvoir la diffusion du matériel publié. Cela permet à IARIA de donner aux articles une visibilité accrue grâce à la distribution, à l'inclusion dans les bibliothèques et à des arrangements pour la soumission à des index.")
    st.write("Remplissez le formulaire ci-dessous et cliquez sur le bouton Soumettre, qui ouvrira une nouvelle fenêtre pour la complétion de la cession de droits d'auteur.")
    if st.button("Passer à l'Étape 7"):
        st.success("Étape 6 complétée.")



    # Étape 7: Soumission du fichier PDF
    st.header("Étape 7: Soumission du fichier PDF")

    # Formulaire de soumission du PDF
    # Étape 7: Soumission du fichier PDF
    your_full_name = st.text_input("Votre nom complet:", key="unique_key_name")
    your_email = st.text_input("Votre adresse e-mail", key="unique_key_email")
    your_code =st.text_input("Your confirmation code", key="unique_key_code")
    article_title = st.text_input("Titre de l'article", key="unique_key_article")
    main_topic = st.selectbox("Main Topic", main_topics, key="unique_key_topic")
    copyright_completed = st.checkbox(
        "La cession de droits d'auteur est complétée")
    
    pdf_file = st.file_uploader(
        "Sélectionnez le fichier PDF (max 8Mo)")
        
     
    if pdf_file and st.button("Soumettre le PDF"):
        pdf_content_base64 = base64.b64encode(pdf_file.getvalue()).decode()
        data = (
            your_full_name, your_email, article_title, main_topic,
            copyright_completed, pdf_content_base64
        )
        # Appel de la fonction avec le code de confirmation et l'e-mail
        insert_pdf_into_snowflake(cursor, data, your_code, your_email)
        process_pdf_analysis(pdf_file)
        
    elif not pdf_file and st.button("Soumettre le PDF"):
        st.error("Veuillez télécharger un fichier PDF")

#paiement
paypalrestsdk.configure({
    "mode": "sandbox",  # Changez à "live" pour la production
    "client_id": "AedG7hgccoHVoznGOI2ecKeaz1ZAwpWAtWQGVj4txAWrfyYWx4e3bUBzhpIWFJlhWZSqDpirm8lKyxkM",
    "client_secret": "EMb3D4rH8rJNUWm4a0LdCyYZTWYXBf4kKGzue-Q4rZL8rI1adXqJOaG4RUFmuS9Jwq81cJZQRpsIlrvQ"
})

# Fonction pour créer un paiement
def create_payment(total_price):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8501/",  # Remplacez par votre URL de succès
            "cancel_url": "http://localhost:8501/"    # Remplacez par votre URL d'annulation
        },
        "transactions": [{
            "amount": {
                "total": str(total_price),   # Montant total du paiement
                "currency": "CAD"
            },
            "description": "Paiement pour soumission d'article scientifique"
        }]
    })

    if payment.create():
        return payment
    else:
        return None

# Fonction pour la page de paiement
def show_payment_page(registration_info):
    st.title("Payment")
    
    st.title("Soumettre un article - Paiement PayPal")

    # Informations sur l'article
    st.header("Détails de l'article")
    st.subheader("Titre : Article scientifique")
    st.subheader(f"Prix : {registration_info['total_price']} $ (taxes incluses)")   
    st.subheader("Description : Soumettez votre article en effectuant le paiement.")

    # Bouton pour effectuer le paiement
  
        # Créer le paiement
    payment = create_payment(registration_info['total_price'])
    if payment:
        approval_url = next(link.href for link in payment.links if link.rel == 'approval_url')
        st.markdown(f"Cliquez [ici]({approval_url}) pour finaliser le paiement.")
    else:
        st.error("Une erreur s'est produite lors de la création du paiement.")

# Fonction pour la page d'inscription





def show_inscription_page():
    # Définir la réponse au défi "To prove you are not a robot"
    challenge_response = "13"  # La réponse correcte est "13"
 
    # Définir un titre pour votre application Streamlit
    st.title("ACADEMIC PUBLISH 2023 - Submit a New Contribution")
 
    # Créer le formulaire de soumission
    contribution_title, track_preference, main_topic, contribution_type, content_type, challenge_answer = submit_contribution()
 
    # Formulaire pour l'auteur principal
    st.subheader("Author Information (Contact Author):")
    contact_author, author_email, first_name, last_name, institution, country = submit_contribution_author()
 
    # Définir le motif pour vérifier le format de l'e-mail
    email_pattern = r'^[\w\.-]+@[\w\.-]+(\.\w+)+$'
 
    # Liste pour les autres auteurs
    st.subheader("Additional Authors:")
    num_additional_authors, additional_authors = submit_additional_authors()
 
    # Champ pour l'abstract
    abstract = st.text_area("Abstract")
 
    # Liste des topics
    # st.subheader("Topics")
    #main_topic_options = g_main_topics()
    #selected_topics = st.multiselect("Select Topics", main_topic_options)
   
    # Boutons Submit et Reset
    if st.button("Submit Contribution"):
        if (
            contribution_title
            and track_preference
            and main_topic
            and contribution_type
            and content_type
            and challenge_answer == challenge_response
            and first_name
            and last_name
            and institution
            and re.match(email_pattern, author_email)  # Vérification de l'e-mail de l'auteur principal
        ):
            try:
               # Enregistrez les données de la contribution dans la base de données ou un autre système de stockage
               confirmation_code = send_confirmation_email(author_email, first_name)
               save_contribution_data_snowflake(contribution_title, track_preference, main_topic, contribution_type, abstract, content_type, author_email, confirmation_code)
 
               # Affichez les informations soumises en bas de la page
               show_submitted_informations(contribution_title, track_preference, main_topic, contribution_type, content_type,
                                        author_email, first_name, last_name, institution, country,
                                        additional_authors, abstract)
 
               st.success(f"Contribution '{contribution_title}' submitted successfully.")
               st.info("Please check your email for further instructions.")
            except Exception as e:
               st.error(f"An error occurred while processing the contribution: {str(e)}")
        else:
            st.error("Please fill in all required fields and pass the challenge.")
    # Bouton Reset
    if st.button("Reset"):
        st.experimental_rerun()
    # Modify
    
    # Ajouter un bouton "Modifier"
    




def get_existing_titles_from_snowflake():
    existing_titles = []

    try:
        # Connectez-vous à Snowflake (remplacez les paramètres par les vôtres)
        connection = snowflake.connector.connect(
            user='christiane',
            password='Kkcv2002@gkmm',
            account='rwwrqgg-fb48745',
            warehouse='COMPUTE_WH',
            database='RCWPROJET',
            schema='CHRISTIANE'
        )

        # Créez un curseur pour exécuter des requêtes SQL
        cursor = connection.cursor()

        # Exécutez une requête pour récupérer les titres depuis la table "contributions"
        cursor.execute("SELECT contribution_title FROM contribution")

        # Récupérez les résultats de la requête
        results = cursor.fetchall()

        # Ajoutez les titres à la liste existing_titles
        existing_titles = [result[0] for result in results]

    except Exception as e:
        print(f"Erreur lors de la récupération des titres depuis Snowflake : {e}")

    finally:
        # Fermez la connexion à Snowflake
        if connection:
            connection.close()

    return existing_titles


# ... (autre code existant)

    # ...

    # Bouton Reset
 

# Fonction pour la page d'inscription 






def show_registration_page():
    st.title("Registration and Payment")
    

    # Section de confirmation de l'email0000
    st.header("Email Confirmation")

    # Entrée du code de confirmation
    confirmation_code_input = st.text_input("Enter Confirmation Code")
    email_input = st.text_input("Enter Email for Confirmation")

    # Bouton de confirmation
    if st.button("Confirm Email"):
        confirm_email(confirmation_code_input, email_input)
    st.title("Registration Form")
    # Formulaire d'inscription
    email = st.text_input("Email")
    title = st.text_input("Title")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    institution = st.text_input("Institution")
    country = st.text_input("Country")
    street_address = st.text_input("Street Address")
    city = st.text_input("City")
    state = st.text_input("State")
    postal_code = st.text_input("Postal Code")
    phone = st.text_input("Phone")
    fax = st.text_input("Fax")
    vat = st.text_input("VAT")
    about_conference = st.text_area("About Conference")

    # Bouton de soumission du formulaire
    if st.button("Submit"):
        save_to_database(email, title, first_name, last_name, institution, country,
                          street_address, city, state, postal_code, phone, fax, vat, about_conference)
        st.success("Registration submitted successfully!")
    

    # Section d'inscription
    st.header("Registration")

    selected_registration = st.selectbox(
        "Select Registration",
        [
            "Select Registration",
            "Registration iaria fellow - 64 CAD",
            "Registration Full time student - 64 CAD",
            "Registration Academic - 95 CAD",
            "Registration Industry - 83 CAD"
        ]
    )

    # Section d'options supplémentaires
    st.header("Additional Options")
    extra_pages = st.selectbox("Extra Pages (105 CAD per page over 6 pages)", list(range(7)), format_func=lambda x: 'No extra pages' if x == 0 else f"{x} extra pages")
    extra_gala_dinners = st.selectbox("Extra Gala Dinners (95 CAD, needed for accompanying persons)", list(range(4)), format_func=lambda x: 'No extra dinners' if x == 0 else f"{x} extra dinner(s)")

    # Bouton d'inscription
   

# Bouton d'inscription
    if st.button("Submit Registration"):
        # Calculer le prix total en utilisant la fonction calculate_total_price
        total_price = calculate_total_price(selected_registration, extra_pages, extra_gala_dinners)

    # Enregistrer les informations d'inscription
        save_registration_info(confirmation_code_input, selected_registration, extra_pages, extra_gala_dinners)

    # Informations de la page d'inscription
        
   

    # Afficher un message avec le prix total
        st.success(f"Your registration has been submitted successfully! Total Price: {total_price} CAD")
        registration_info = {
            'total_price': total_price
        }

        # Section de paiement
        show_payment_page(registration_info)
# ...


    
    
    #show_payment_page()
        
    def redirect_to_paypal_page():
        st.markdown("[Go to PayPal Page](./pages/paypal.html)")

# Afficher le bouton dans Streamlit

# Note: Assurez-vous d'avoir les fonctions confirm_email, save_registration_info, et save_payment_info définies dans votre code.

# Fonction principale
def main():
    # Titre de l'application
    st.title("ACADEMIC PUBLISH")

    # Titre de la barre latérale
    st.sidebar.title("CHOOSE YOUR PAGE")

    # Liste déroulante pour la navigation sur la gauche
    selected_page = st.sidebar.selectbox("", ["Home", "SUBMIT A CONTRIBUTION", "REGISTER","Camera Ready","READ ARTICLES"])

    # Afficher le contenu en fonction de la page sélectionnée
    if selected_page == "Home":
        st.write("WELCOME TO YOUR PLATFORM TO SUBMIT YOUR SCIENTIFIC ARTICLE")
    elif selected_page == "SUBMIT A CONTRIBUTION":
        show_inscription_page()
    elif selected_page == "REGISTER":
        show_registration_page()
    elif selected_page == "Camera Ready":
        show_CR_page()
    elif selected_page == "READ ARTICLES":
        show_articles()    
    elif select_pdf_file=="":
        st.write("WELCOME TO YOUR PLATFORM TO SUBMIT YOUR SCIENTIFIC ARTICLE")

# Exécutez l'application
if __name__ == "__main__":
    main()
