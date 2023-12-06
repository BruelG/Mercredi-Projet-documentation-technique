import pandas as pd
import streamlit as st
import requests
from streamlit_option_menu import option_menu
import snowflake.connector as sf
from datetime import datetime
from decimal import Decimal 
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from streamlit_chat import message
import os
import faiss
from PIL import Image

sidebar = st.sidebar
session_state = st.session_state

def welcome(prenom,nom):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_hour = int(current_time.split(':')[0])
    
    if 6 <= current_hour < 12:
        st.header(f"Bonjour {prenom} {nom} !")
    elif 12 <= current_hour < 18:
        st.header(f"Bon après-midi {prenom} {nom} !")
    else:
        st.header(f"Bonsoir {prenom} {nom} !")
cacheWelcome = st.cache_data(welcome)

def connectSno():
    snowflake_config = {
        'user': 'MICIJOZAA',
        'password': '!0Micijoza',
        'account': 'uu64700.ca-central-1.aws',
        'warehouse': 'COMPUTE_WH',
        'database': 'DOCUMENTATION',
        'schema': 'MICIJOZA'
    }
    try:
        conn = sf.connect(**snowflake_config)
        cs = conn.cursor()
        st.session_state['snow_con'] = cs
        st.session_state['is_ready'] = True
        return conn
    except Exception as e:
        return st.error("Failed connection to SnowFlake")
cacheConnectSnow = st.cache_data(connectSno)

if 'is_ready' not in st.session_state:
    st.session_state['is_ready'] = False

def get_sessions():
    if not st.session_state.get('is_ready'):
        connectSno()
    conn = st.session_state.get('snow_con')
    if conn:
        conn.execute("SELECT * FROM sessions")
        sessions = conn.fetchall()  # Liste de tuples (ID, NOMDELASESSION)
        sessions.reverse()
        return sessions
    else:
        st.error("La session Snowflake n'est pas prête. Assurez-vous de vous connecter d'abord.")
get_sessions = st.cache_data(get_sessions)

def get_cours(id, session):
    if not st.session_state.get('is_ready'):
        connectSno()
    conn = st.session_state.get('snow_con')
    if conn:
        conn.execute(f"SELECT * FROM COURS WHERE ENSEIGNANTID = {id} AND SESSIONID = {session}")
        cours = conn.fetchall()
        return cours
    else:
        st.error("La session Snowflake n'est pas prête. Assurez-vous de vous connecter d'abord.")
get_cours = st.cache_data(get_cours)

def get_groups(cours_id):
    if not st.session_state.get('is_ready'):
        connectSno()
    conn = st.session_state.get('snow_con')
    if conn:
        query = f"SELECT NOMDUGROUPE FROM GROUPES WHERE GROUPEID IN (SELECT GROUPEID FROM COURSGROUPES WHERE COURSID = {cours_id})"
        groupes = conn.execute(query).fetchall()
        groupes = [g[0] for g in groupes]
        print(groupes)
        return groupes
    else:
        st.error("La session Snowflake n'est pas prête. Assurez-vous de vous connecter d'abord.")
get_groups = st.cache_data(get_groups)

def connectEtud(user, pwd):
    if not st.session_state['is_ready']:
        connectSno()
    conn = st.session_state.get('snow_con')
    if conn:
        conn.execute(f"SELECT * FROM ETUDIANTS WHERE NUMERODA = '{user}' AND MOTDEPASSE = '{pwd}'")
        result = conn.fetchone()
        if result:
            etudiant_data = {
                "id": result[0],
                "nom": result[1],
                "prenom":result[2],
                "da":result[4],
                "codePermanent":result[5]
            }
            st.session_state['etudiant_data'] = etudiant_data
            st.session_state['id'] = etudiant_data["id"]
            st.session_state['nom'] = etudiant_data["nom"]
            st.session_state['prenom'] = etudiant_data["prenom"]
            st.session_state['prof_ready'] = False
            st.session_state['etudiant_ready'] = True
            
        else:
            return st.error("error : Étudiant non trouvé")
    else:
        st.error("La session Snowflake n'est pas prête. Assurez-vous de vous connecter d'abord.")
cacheConnectEtud = st.cache_data(connectEtud)

def connectProf(user, pwd):
    if not session_state.get('is_ready'):
        connectSno()
    conn = session_state.get('snow_con')
    if conn:
        try:
            conn.execute(f"SELECT * FROM ENSEIGNANTS WHERE NUMEROPROF = %s AND MOTDEPASSE = %s", (user, pwd))
            result = conn.fetchone()
            if result:
                enseignant_data = {
                    "id": result[0],
                    "nom": result[1],
                    "prenom": result[2],
                    "num": result[4],
                    "nas": result[5]
                }
                st.session_state['enseignant_data'] = enseignant_data
                st.session_state['id'] = enseignant_data["id"]
                st.session_state['nom'] = enseignant_data["nom"]
                st.session_state['prenom'] = enseignant_data["prenom"]
                st.session_state['prof_ready'] = True
                st.session_state['etudiant_ready'] = False
            else:
                st.error("error : Enseignant non trouvé")
        except Exception as e:
            st.error(f"Une erreur s'est produite : {str(e)}")
    else:
        st.error("La session Snowflake n'est pas prête. Assurez-vous de vous connecter d'abord.")
cacheConnectProf = st.cache_data(connectProf)

def get_note(etudiant, evaluation):
    conn = connectSno()
    cursor = conn.cursor()
    select_query = f"""
    SELECT N.Note
    FROM Etudiants E
    LEFT JOIN Notes N ON E.EtudiantID = N.EtudiantID
    LEFT JOIN Evaluations EV ON N.EvaluationID = EV.EvaluationID
    WHERE E.Nom = '{etudiant}' AND EV.TitreDeLEvaluation = '{evaluation}';
    """
    cursor.execute(select_query)
    result = cursor.fetchone()

    if result:
        return result[0]  # Retourner la note si elle existe
    else:
        return None 

def afficher_evaluations_par_cours(cours_id, group):
    conn = connectSno()
    cursor = conn.cursor()

    # Récupérer les données d'évaluation
    select_query = f"""
    SELECT EvaluationID, TitreDeLEvaluation, Ponderation
    FROM Evaluations
    WHERE COURSID = {cours_id};
    """
    cursor.execute(select_query)
    evaluation_data = cursor.fetchall()

    if not evaluation_data:
        st.info("Aucune évaluation trouvée pour le cours avec l'ID spécifié.")
        return

    noms_evaluations = [f"{row[1]}\n({row[2]})" for row in evaluation_data]
    etudiants, notes_etudiants = get_etudiants_et_notes(cours_id, group)
    df = pd.DataFrame.from_dict(notes_etudiants, orient='index')
    df.columns = noms_evaluations
    df = df.fillna(0)
    max_row = pd.DataFrame(df.max()).transpose().rename(index={0: 'Note maximale'})
    df = pd.concat([df, max_row])
    placeholder = st.empty()
    placeholder.write(df)
    col1,col2 = st.columns(2)
    with col1:
        if st.button("Modifier") or st.session_state.get("modifier_clicked", False):
            st.session_state['modifier_clicked'] = True
            placeholder.empty()
            modifier_notes(df, etudiants, noms_evaluations, notes_etudiants)
            
            
    with col2:
        if st.button("Voir résultats"):
            st.session_state['modifier_clicked'] = False
            df['Moyenne'] = df.mean(axis=1, skipna=True)

            df['Mention'] = pd.cut(df['Moyenne'], bins=[0, 60, 63, 67, 70, 73, 77, 80, 85, 90, 100], labels=['E', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+'])

            placeholder.write(df)

def update_notes(etudiant, evalid, note):
    conn = connectSno()
    cursor = conn.cursor()
    nom, prenom = etudiant.split(" ")
    query_etudiant_id = f"SELECT EtudiantID FROM Etudiants WHERE Nom = '{nom}' AND Prenom = '{prenom}'"
    cursor.execute(query_etudiant_id)
    etudiant_id = cursor.fetchone()[0]
    idEval = evalid+1
    if 0 <= float(note) <= 100:
        query_update_note = f"UPDATE NOTES SET NOTE = {note} WHERE ETUDIANTID = {etudiant_id} AND EVALUATIONID = {idEval}"
        cursor.execute(query_update_note)
        conn.commit()
        cursor.close()
        conn.close()
    else:
        st.error("The mark should be between 0 and 100")

def modifier_notes(df, etudiants, noms_evaluations, notes_etudiants):
    st.header("Modifier les notes")
    cols = st.columns(len(noms_evaluations))
    for j, nom_evaluation, col in zip(range(len(noms_evaluations)), noms_evaluations, cols):
        col.write(f":blue[{nom_evaluation}]")
        st.write(" ")
        for i, etudiant in enumerate(etudiants):
            default_value = Decimal('0.0') 
            if etudiant in notes_etudiants and j < len(notes_etudiants[etudiant]):
                default_value = notes_etudiants[etudiant][j]
            updated_value = col.text_input(label=f"{etudiant}", key=f"{etudiant}_{j}_{i}",value=default_value)
            if etudiant not in notes_etudiants:
                notes_etudiants[etudiant] = [Decimal('0.0')] * len(noms_evaluations)
            notes_etudiants[etudiant][j] = updated_value
    if 'modifier_clicked' in st.session_state and st.session_state['modifier_clicked']:
        if st.button("Modifier les notes"):
            for etudiant, notes in notes_etudiants.items():
                for j, note in enumerate(notes):
                    if 0 <= float(note) <= 100:
                        update_notes(etudiant, j, note)
            
            st.session_state['modifier_clicked'] = False
            st.success("Les notes ont été modifiées avec succès!")
   
def notes2Etudiant(idEt, selected_session):
    conn = connectSno()
    cursor = conn.cursor()
    query_courses = """
        SELECT DISTINCT C.TitreDuCours
        FROM Cours C
        INNER JOIN Sessions S ON C.SessionID = S.SessionID
        WHERE S.NomDeLaSession = %s
    """
    cursor.execute(query_courses, (selected_session,))
    list_of_courses = [row[0] for row in cursor.fetchall()]

    # Check if there are courses for the selected session
    if not list_of_courses:
        st.warning("Aucun cours trouvé pour la session sélectionnée.")
        return

    # Get the selected course from the user
    selected_cours = st.selectbox("Sélectionnez un cours", list_of_courses)

    # Retrieve the notes for the selected student and course
    query_notes = """
        SELECT E.EvaluationID, E.TitreDeLEvaluation, N.Note
        FROM Cours C
        INNER JOIN Evaluations E ON C.CoursID = E.COURSID
        LEFT JOIN Notes N ON N.EtudiantID = %s AND N.EvaluationID = E.EvaluationID
        WHERE C.TitreDuCours = %s
    """
    cursor.execute(query_notes, (idEt, selected_cours))
    result = cursor.fetchall()

    if result:
        st.info(f"Voici les notes de l'étudiant pour le cours {selected_cours} dans la session {selected_session}:")
        for row in result:
            evaluation = row[1]
            note = row[2]
            if note is not None:
                st.success(f"Evaluation: {evaluation}, Note: {note}")
            else:
                st.info(f"Pas de note pour l'évaluation: {evaluation}")
    else:
        st.info("Aucune note trouvée pour cet étudiant dans le cours sélectionné.")

def get_etudiants_et_notes(cours_id, group):
    conn = connectSno()
    cursor = conn.cursor()
    select_query = f"""
    SELECT E.Nom, E.Prenom, EV.TITREDELEVALUATION, N.Note
    FROM Etudiants E
    JOIN GROUPES G ON E.GROUPEID = G.GROUPEID
    JOIN COURSGROUPES CG ON G.GROUPEID = CG.GROUPEID
    JOIN Cours C ON CG.CoursID = C.CoursID
    LEFT JOIN Notes N ON E.EtudiantID = N.EtudiantID
    LEFT JOIN Evaluations EV ON C.CoursID = EV.COURSID AND N.EvaluationID = EV.EvaluationID
    WHERE C.CoursID = {cours_id} AND G.NOMDUGROUPE = '{group}';
    """
    cursor.execute(select_query)
    student_data = cursor.fetchall()
    etudiants = []
    notes_etudiants = {}

    for row in student_data:
        nom_etudiant = f"{row[0]} {row[1]}"
        nom_evaluation = row[2]
        note = row[3]
        if nom_etudiant not in etudiants:
            etudiants.append(nom_etudiant)
        if nom_etudiant not in notes_etudiants:
            notes_etudiants[nom_etudiant] = []
        notes_etudiants[nom_etudiant].append(note)
    return etudiants, notes_etudiants

def diagramme(idEt, selected_session):
    conn = connectSno()
    cursor = conn.cursor()
    query_courses = """
    SELECT DISTINCT C.TitreDuCours
    FROM Cours C
    INNER JOIN Sessions S ON C.SessionID = S.SessionID
    WHERE S.NomDeLaSession = %s
    """
    cursor.execute(query_courses, (selected_session,))
    courses = cursor.fetchall()
    query_average = """
    SELECT AVG(N.Note) AS Moyenne
    FROM Cours C
    INNER JOIN Evaluations E ON C.CoursID = E.COURSID
    LEFT JOIN Notes N ON N.EtudiantID = %s AND N.EvaluationID = E.EvaluationID
    WHERE C.TitreDuCours = %s
    """
    course_titles = []
    averages = []

    for course in courses:
        course_title = course[0]
        cursor.execute(query_average, (idEt, course_title))
        average_result = cursor.fetchone()
        course_titles.append(course_title)
        averages.append(round(average_result[0], 2) if average_result[0] is not None else None)
    for i, (course_title, avg) in enumerate(zip(course_titles, averages)):
        if 90 <= avg <= 100:
            st.success(f"Bravo! Vous avez obtenu une excellente moyenne ({avg}) dans le cours {course_title}. Si vous êtes intéressé par le tutorat, veuillez contacter l'administration.")
        elif avg < 60:
            st.warning(f"Votre moyenne ({avg}) dans le cours {course_title} est inférieure à 60. Il est recommandé de suivre le tutorat.")
        else:
            st.info(f"Votre moyenne ({avg}) dans le cours {course_title} est dans une plage normale. Continuez votre bon travail!")

    # Création du diagramme
    fig, ax = plt.subplots()
    x = np.arange(len(course_titles))

    # Changer la couleur en vert si la moyenne est supérieure à 60, sinon rouge
    colors = ['green' if avg > 60 else 'red' for avg in averages]

    # Réduire la taille des barres
    bar_width = 0.5  # Vous pouvez ajuster cette valeur selon vos préférences
    ax.bar(x, averages, align='center', alpha=0.7, color=colors, width=bar_width)
    
    ax.set_xticks(x)
    ax.set_xticklabels(course_titles, rotation=45, ha='right')
    ax.set_ylim(0, 100)
    ax.set_ylabel('Moyenne des notes')
    ax.set_title('Moyenne des notes par cours')

    # Affichage du diagramme
    st.pyplot(fig)

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    # End extraction
    # Start chunks breakdown
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1400,
        chunk_overlap=320,
        length_function=len
    )
    chunks = splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings() #c kom BIT, HARALICK...
    vectorstores = FAISS.from_texts(embedding = embeddings, texts = text_chunks) 
    return vectorstores
   
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = None
def handle_user_input(inputT):
    if st.session_state.conversation is None:
        pdf_folder = "./pdfs/"
        pdf_files = [os.path.join(pdf_folder, file) for file in os.listdir(pdf_folder) if file.endswith(".pdf")]
        raw_text = get_pdf_text(pdf_files)
        text_chunks = get_text_chunks(raw_text)
        vectorstore = get_vectorstore(text_chunks) 
        st.session_state.pdf_processed = True
        st.session_state.conversation = get_conversation_chain(vectorstore)
    answer = st.session_state.conversation({'question': inputT})
    st.session_state.chat_history = answer['chat_history']
    for i, msg in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            message(msg.content, is_user=True, key=str(i) + '_user', logo='https://media.licdn.com/dms/image/D4E03AQFxfygYgjoDyQ/profile-displayphoto-shrink_400_400/0/1700864064492?e=1707350400&v=beta&t=fdhevo9tpfQzhTdgKnQpzb0DJcMcD8cLLNkfHT5OEKg')
        else:
            message(msg.content, key=str(i), logo="https://www.techrepublic.com/wp-content/uploads/2023/07/tr71123-ai-art.jpeg")

def get_conversation_chain(vectors):
    current_llm = ChatOpenAI()
    current_memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True
    )
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=current_llm,
        retriever=vectors.as_retriever(),
        memory=current_memory
    )
    return conversation_chain

menuu = option_menu(
    menu_title=None,
    options=["Recherche manuelle", "Assistant virtuel"],
    icons=["person", "robot"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
)
if 'prof_ready' not in st.session_state:
        st.session_state['prof_ready'] = False
if 'etudiant_ready' not in st.session_state:
    st.session_state['etudiant_ready'] = False
if menuu == "Recherche manuelle":
    if st.session_state['etudiant_ready'] == True:
        welcome(st.session_state['prenom'], st.session_state['nom'])
        sessions = get_sessions()
        sess = st.selectbox("Sélectionnez une session",[ses[2] for ses in sessions])
        selected_session_id = [session[0] for session in sessions if session[2] == sess][0]
        with st.expander(f"Checker l'horaire"):
            st.info("Pas d\'informations valides")
        with st.expander(f"Consulter mes notes"):
            notes2Etudiant(st.session_state['id'],sess)
        with st.expander(f"Consulter le sommaire des notes"):
            diagramme(st.session_state['id'],sess)
    if st.session_state['prof_ready'] == True:
        welcome(st.session_state['prenom'], st.session_state['nom'])
        sessions = get_sessions()
        sess = st.selectbox("Sélectionnez une session",[ses[2] for ses in sessions], index=3)
        selected_session_id = [session[0] for session in sessions if session[2] == sess][0]
        with st.expander(f"Liste des cours"):
            cours = get_cours(st.session_state['enseignant_data']['id'],selected_session_id)
            if cours:
                for cour in cours:
                    titre = cour[1]
                    st.write(f"- {titre}")
                    cours_id = cour[0]
                    structure_modifiee = cour[5]
                    if structure_modifiee == False:
                        struct = st.markdown(f':red[>> [Modifier la structure de l\'evaluation](http://localhost:8502?page=2&cours_id={cours_id})]')  
                        groupes = get_groups(cours_id)
                        selected_groupe = st.selectbox(">>Sélectionnez un groupe", groupes)
                        
                        afficher_evaluations_par_cours(cours_id,selected_groupe)
                    else:
                        struct = st.markdown(f':red[>>[Modifier la structure de l\'evaluation](http://localhost:8502?page=2&cours_id={cours_id})]')

            else:
                st.success("Vous avez pas cours cette session")
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = None
if 'conversation' not in st.session_state:
    st.session_state.conversation = None
if menuu == "Assistant virtuel":
    load_dotenv() 
    user_question = st.text_input("Ask your questions...")
    if user_question:
        handle_user_input(user_question)
    pdf_folder = "./pdfs/"
    pdf_files = [os.path.join(pdf_folder, file) for file in os.listdir(pdf_folder) if file.endswith(".pdf")]
    raw_text = get_pdf_text(pdf_files)
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(text_chunks) 
    st.session_state.pdf_processed = True
    st.session_state.conversation = get_conversation_chain(vectorstore)
            
with sidebar:
    
    st.write(
    f"""
    <style>
        .stCenterHorizontal {{
            display: flex;
            justify-content: center;
        }}
        .stCustomText {{
            font-family: fantasy;
            font-size: 36px; 
            color: #DECC80;
        }}
    </style>
    <div class="stCenterHorizontal">
        <p class="stCustomText">m i c i j o z a</p>
    </div>
    """,
    unsafe_allow_html=True
    )
    selected = option_menu(
        menu_title=None,
        options=["Enseignant", "Etudiant"],
        icons=["person-check", "mortarboard"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )
    if selected == "Enseignant":
        st.empty()
        user = st.text_input('No d\'enseignant', type="password")
        pwd = st.text_input('Password', type="password")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            connect = st.button('C o n n e c t', key="connect_button", on_click=connectProf, args=[
                user, pwd
            ])
        col4, col5, col6 = st.columns([0.95, 1.65, 0.90])
        with col5:
            auth = st.markdown('[Première utilisation ?](http://localhost:8511/)')
            forgot = st.markdown('[Mot de passe oublié ?](http://localhost:8503/)')
    if selected == "Etudiant":
        st.empty()
        user = st.text_input('No de DA', type="password")
        pwd = st.text_input('Password', type="password")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            connect = st.button('C o n n e c t', on_click=connectEtud, args=[
            user, pwd
            ])
        col4, col5, col6 = st.columns([0.95, 1.65, 0.90])
        with col5:
            auth = st.markdown('[Première utilisation ?](http://localhost:8505/)')
            forgot = st.markdown('[Mot de passe oublié ?](http://localhost:8508/)')
        
       