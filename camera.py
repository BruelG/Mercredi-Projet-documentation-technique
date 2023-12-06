import streamlit as st
import snowflake.connector
import base64
from email.message import EmailMessage
import ssl
import smtplib
import PyPDF2
import uuid
import spacy
from textstat import coleman_liau_index
from sklearn.metrics.pairwise import cosine_similarity

# Configuration initiale de la page
main_topics = ["Academic Publish 2023 :Cloud", "Academic Publish 2023 :Data", "Academic Publish 2023 :Energy",
               "Academic Publish 2023 :Health", "Academic Publish 2023 :Human-Machine", "Academic Publish 2023 :Intelligence",
               "Academic Publish 2023 :Internet", "Academic Publish 2023 :IoT", "Academic Publish 2023 :Learning",
               "Academic Publish 2023 :Meta verse", "Academic Publish 2023 :Mobility", "Academic Publish 2023 :Multimedia"]
# CSS personnalisé pour améliorer le style
#Email:
def send_confirmation_email(author_email, first_name):
    confirmation_code = str(uuid.uuid4())[:8].upper()
    confirmation_message = f"""
            Dear {first_name},

            Thank you for submitting your scientific 
            article with our platform. We are pleased to confirm 
            that your article  was submitted succesfully.

            If you have any questions or need further
            assistance, feel free to contact our support team.

            Best regards,
            Publish
            """

    msg = EmailMessage()
    msg.set_content(confirmation_message)
    msg["Subject"] = "Academic Publish 2023 Contribution Submission Confirmation"
    msg["From"] = "publishour@gmail.com"  # Remplacez par votre adresse e-mail
    msg["To"] = author_email

    # Configuration du serveur SMTP (Gmail dans cet exemple)
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    smtp_username = "publishour@gmail.com"  # Remplacez par votre adresse e-mail Gmail
    smtp_password = "yoyi onqp eopn rcpu"  # Remplacez par votre mot de passe Gmail
    context = ssl.create_default_context()

    # Envoi de l'e-mail
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

    return confirmation_code


# Fonction pour établir la connexion à Snowflake


def connect_to_snowflake():
    snowflake_config = {
        "user": "christiane",
        "password": "Kkcv2002@gkmm",
        "account": "rwwrqgg-fb48745",
        "warehouse": "COMPUTE_WH",
        "database": "RCWPROJET",
        "schema": "CHRISTIANE"
    }
    return snowflake.connector.connect(**snowflake_config)

# Fonction pour insérer le PDF dans Snowflake


def insert_pdf_into_snowflake(cursor, data, confirmation_code, author_email):
    try:
        # Vérifier la correspondance dans la table CONTRIBUTION
        cursor.execute("""
            SELECT COUNT(*)
            FROM RCWPROJET.CHRISTIANE.CONTRIBUTION
            WHERE CODE_CONFIRMATION = %s AND CHER_EMAIL = %s
        """, (confirmation_code, author_email))
        result = cursor.fetchone()
        if result[0] > 0:
            # Correspondance trouvée, procédez à l'insertion dans Snowflake
            cursor.execute("""
                INSERT INTO RCWPROJET.CHRISTIANE.CAMERAREADY (
                    YOUR_FULL_NAME, YOUR_EMAIL, ARTICLE_TITLE, ARTICLE_TOPIC, COPYRIGHT_COMPLETED, PDF_CONTENT_BINARY
                )
                VALUES (%s, %s, %s, %s, %s, TO_BINARY(%s, 'BASE64'))
            """, data)
            cursor.connection.commit()
            st.success("Données enregistrées avec succès dans Snowflake.")
            send_confirmation_email(author_email, data[0])  # Envoie de l'e-mail de confirmation
        else:
            # Pas de correspondance trouvée, affichez un message d'erreur
            st.error("Le code de confirmation ou l'e-mail est incorrect.")
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement dans Snowflake: {e}")



# # Connexion à Snowflake
# conn = connect_to_snowflake()
# cursor = conn.cursor()

# # En-tête
# st.markdown('<p class="big-font">Camera Ready - Processus de Soumission</p>',
#             unsafe_allow_html=True)

# # Définition des étapes
# etapes = [
#     "Enregistrement de l'article",
#     "Délais",
#     "Contenu",
#     "Formatage",
#     "Production du PDF",
#     "Cession de droits d'auteur",
#     "Soumission du fichier PDF"
# ]

# for i, etape in enumerate(etapes, start=1):
#     with st.container():
#         st.header(f"Étape {i}: {etape}")

#         if i < 7:
#             if st.button(f"Passer à l'Étape {i+1}", key=f"button{i}"):
#                 st.success(f"Étape {i} complétée.")
#         else:
#             # Étape 7: Soumission du fichier PDF
#             your_full_name = st.text_input("Votre nom complet:", key="unique_key_name")
#             your_email = st.text_input("Votre adresse e-mail", key="unique_key_email")
#             article_title = st.text_input("Titre de l'article", key="unique_key_article")
#             main_topic = st.selectbox("Main Topic", main_topics, key="unique_key_topic")
#             copyright_completed = st.checkbox(
#                 "La cession de droits d'auteur est complétée")
    
#             pdf_file = st.file_uploader(
#                 "Sélectionnez le fichier PDF (max 8Mo)")
#             your_code =st.text_input("Your confirmation code", key="unique_key_code")
            
#             if pdf_file and st.button("Soumettre le PDF"):
#               pdf_content_base64 = base64.b64encode(pdf_file.getvalue()).decode()
#               data = (
#                 your_full_name, your_email, article_title, main_topic,
#                 copyright_completed, pdf_content_base64
#               )
#               # Appel de la fonction avec le code de confirmation et l'e-mail
#               insert_pdf_into_snowflake(cursor, data, your_code, your_email)
#             elif not pdf_file and st.button("Soumettre le PDF"):
#                st.error("Veuillez télécharger un fichier PDF")

# Chargez le modèle en français de spaCy
nlp = spacy.load("fr_core_news_sm")

def select_pdf_file():
    # Fonction pour sélectionner un fichier PDF
    file_path = st.file_uploader("Upload a PDF file", type=["pdf"])
    return file_path

def calculer_pourcentage_lisibilite(indice_coleman_liau, min_val, max_val):
    # Fonction pour calculer le pourcentage de lisibilité
    indice_coleman_liau = max(min_val, min(max_val, indice_coleman_liau))
    pourcentage_normalise = ((indice_coleman_liau - min_val) / (max_val - min_val)) * 100
    return pourcentage_normalise

def calculer_similarite_semantique(doc):
    # Fonction pour calculer la similarité sémantique
    vecteurs_phrases = [sent.vector for sent in doc.sents]
    sim_matrix = cosine_similarity(vecteurs_phrases)
    sim_moyenne = sim_matrix.mean()
    return sim_moyenne

def process_pdf_analysis(pdf_path):
    with pdf_path as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        pdf_content = ""
        for page_num in range(len(pdf_reader.pages)):
            pdf_content += pdf_reader.pages[page_num].extract_text()

        # Traitez le texte avec spaCy
        doc = nlp(pdf_content)
        
        # Ajoutez l'extension 'polarity' à spaCy si elle n'a pas déjà été ajoutée
        if not doc.has_extension('polarity'):
            spacy.tokens.Doc.set_extension('polarity', default=None)

        # Afficher le contenu du PDF
        st.header("Contenu du PDF :")
        st.text(pdf_content)

        # Analyse de la clarté
        coleman_liau_score = coleman_liau_index(pdf_content)

        # Analyse de la longueur des phrases et des paragraphes
        sentence_lengths = [len(sent) for sent in doc.sents]
        average_sentence_length = sum(sentence_lengths) / len(sentence_lengths)

        # Précision: Analyse de sentiment
        # spaCy fournit une mesure de polarité

        # Richesse du vocabulaire
        unique_words = set(token.text.lower() for token in doc if token.is_alpha)
        total_words = len(doc)
        lexical_diversity = len(unique_words) / total_words

        # Similarité sémantique
        similarity_score = calculer_similarite_semantique(doc)

        # Affichage des résultats avec Streamlit
        st.header("Analyse de la clarté avec l'indice Coleman-Liau:")
        pourcentage_resultat = calculer_pourcentage_lisibilite(coleman_liau_score, 0, 20)
        st.write(f"L'indice Coleman-Liau de {coleman_liau_score} correspond à un pourcentage de lisibilité de {pourcentage_resultat:.2f}%.")

        st.header("Analyse de la richesse du vocabulaire :")
        lexical_diversity = lexical_diversity * 100
        st.write(f"Diversité lexicale (TTR) de {lexical_diversity:.2f}%.")

        st.header("Cohérence :")
        similarity_score = similarity_score * 100
        st.write(f"Similarité sémantique moyenne: {similarity_score:.4f}%")
        