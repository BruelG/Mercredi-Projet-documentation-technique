import streamlit as st
import snowflake.connector
import pandas as pd


snowflake_config = {
    "user": "christiane",
    "password": "Kkcv2002@gkmm",
    "account": "rwwrqgg-fb48745",
    "warehouse": "COMPUTE_WH",
    "database": "RCWPROJET",
    "schema": "CHRISTIANE"
}

# Fonction principale


def main():
    # Connexion à Snowflake
    conn = snowflake.connector.connect(**snowflake_config)
    cursor = conn.cursor()


# Titre de l'application
st.title("Camera ready - Étapes du processus")

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

# Formulaire de cession de droits d'auteur
your_full_name = st.text_input("Votre nom complet:")
your_email = st.text_input("Votre adresse e-mail")
article_title = st.text_input("Titre de l'article")
article_id = st.text_input("ID de l'article (comme soumis pour l'évaluation)")
copyright_completed = st.checkbox(
    "La cession de droits d'auteur est complétée (Étape 6)")

# Étape 7: PDF file submission
st.header("Étape 7: Soumission du fichier PDF")
st.write("Il est essentiel de prêter attention et d'inclure toutes les informations dans le formulaire ci-dessous. Sur la base de ces données, les listes des procédures et des auteurs seront générées.")
st.write("Veuillez écrire les noms complets des auteurs, en majuscules. N'utilisez pas d'initiales pour le prénom ou le nom de famille. Certains services d'indexation (comme DBLP) nécessitent les noms complets des auteurs. Si des initiales du deuxième prénom sont présentes, veuillez les inclure dans le champ du prénom.")
number_of_pages = st.text_input("Nombre de pages")
keywords = st.text_input("Mots-clés")
abstract = st.text_area("Résumé")
pdf_file = st.file_uploader("Sélectionnez le fichier PDF (max 8Mo)")

if pdf_file:
    st.write("Fichier PDF sélectionné.")
    # Lire le contenu du fichier PDF
    pdf_content = pdf_file.read()
    # Spécifiez le chemin où vous souhaitez enregistrer les fichiers PDF
    pdf_file_path = f"path_to_save_uploaded_pdfs/{pdf_file.name}"

    # Étape 8: The manuscript submission is completed
    st.header("Étape 8: La soumission du manuscrit est terminée")
    st.write("Si tout s'est bien passé, vous devriez avoir reçu deux e-mails : un confirmant la soumission du camera ready et un confirmant la cession de droits d'auteur de l'Étape 6. Si vous n'avez pas reçu ces e-mails dans les quatre heures suivant la fin du processus, veuillez contacter notre équipe PolyglotCodeCrafter@teccart.com.")

    if st.button("Submit"):
        # Utilisez simplement la méthode Binary pour le contenu PDF
        cursor.execute("""
            INSERT INTO RCWPROJET.CHRISTIANE.CAMERAREADY (
                YOUR_FULL_NAME, YOUR_EMAIL, ARTICLE_TITLE, ARTICLE_ID, COPYRIGHT_COMPLETED,
                NUMBER_OF_PAGES, KEYWORDS, ABSTRACT, PDF_CONTENT
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            your_full_name, your_email, article_title, article_id,
            1 if copyright_completed else 0, number_of_pages,
            keywords, abstract, snowflake.connector.Binary(pdf_content)
        ))
        conn.commit()
        st.success("Données enregistrées avec succès dans la table CameraReady.")

    # Fermer la connexion à Snowflake
    cursor.close()
    conn.close()

# Appeler la fonction principale
if __name__ == "__main__":
    main()
