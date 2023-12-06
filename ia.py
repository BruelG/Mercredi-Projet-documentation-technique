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

# Fonctions


def convert_base64_to_bytes(base64_string):
    base64_bytes = base64_string.encode('utf-8')
    decoded_bytes = base64.b64decode(base64_bytes)
    return BytesIO(decoded_bytes)


def pdf_to_text(pdf_content):
    pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_content))
    pdf_text = ""
    for page in pdf_reader.pages:
        pdf_text += page.extract_text()
    return pdf_text


def translate_text(text, dest_language):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    except Exception as e:
        return f"Erreur de traduction: {e}"


def connect_to_snowflake():
    return snowflake.connector.connect(
        user='christiane',
        password='Kkcv2002@gkmm',
        account='rwwrqgg-fb48745',
        warehouse='COMPUTE_WH',
        database='RCWPROJET',
        schema='CHRISTIANE'
    )


def fetch_snowflake_data():
    conn = connect_to_snowflake()
    cur = conn.cursor()
    cur.execute("SELECT * FROM RCWPROJET.CHRISTIANE.CAMERAREADY")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def process_snowflake_data(rows):
    data = [list(x) for x in rows]
    columns = [desc[0] for desc in cur.description]
    df = pd.DataFrame(data, columns=columns)
    return df


def translate_text(text, dest_language):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=dest_language)
        return f"Texte original: '{text}'\nTraduction: '{translation.text}'"
    except Exception as e:
        return f"Erreur de traduction: {e}"


# Exemple d'utilisation
print(translate_text("Bonjour le monde", "en"))


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
        summary_text = response['choices'][0]['text'].strip(
        ) if response and response['choices'] else None

        return summary_text
    except openai.error.RateLimitError as e:
        st.warning(f"Waiting for 20 seconds ")
        time.sleep(20)
        return generate_summary(text)


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

# Définir la clé OpenAI
openai.api_key = mykey

# Convertir les résultats en un DataFrame pandas
data = [list(x) for x in rows]
columns = [desc[0] for desc in cur.description]
df = pd.DataFrame(data, columns=columns)

# Configuration de la page
st.title('READ SCIENTIFIC ARTICLES')

# Transformez le contenu binaire PDF en texte
df['PDF_CONTENT_TEXT'] = df['PDF_CONTENT_BINARY'].apply(
    lambda x: pdf_to_text(x))

# Créer une liste de sujets uniques
unique_topics = list(set(df['ARTICLE_TOPIC']))

# Ajouter l'option "Tous les sujets" à la liste de sujets
unique_topics.insert(0, "Tous les sujets")

# Sélection de sujet avec une liste déroulante
selected_topic = st.selectbox("Select the topic:", unique_topics)

# Filtrer les articles en fonction du sujet sélectionné
if selected_topic == "Tous les sujets":
    selected_articles = df[['YOUR_FULL_NAME',
                            'ARTICLE_TITLE', 'PDF_CONTENT_TEXT']]
else:
    selected_articles = df[df['ARTICLE_TOPIC'] == selected_topic][[
        'YOUR_FULL_NAME', 'ARTICLE_TITLE', 'PDF_CONTENT_TEXT']]

selected_article_info = st.selectbox('Select the article:', selected_articles.itertuples(
    index=False), format_func=lambda x: f"{x[0]}, {x[1]}")

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

# Button for reading the article
if st.button("Read the Article"):
    # Display PDF content in the second column
    col2.subheader("THE ARTICLE")
    col2.text_area(" ", value=selected_article_info[2], height=500)

# Optionally, you can include a button to generate and display the summary

# End of your script
