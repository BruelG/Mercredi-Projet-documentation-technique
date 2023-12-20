import pandas as pd
import streamlit as st
import requests
from streamlit_option_menu import option_menu
import snowflake.connector as sf
from datetime import datetime
from decimal import Decimal 

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
        'account': 'ul81046.ca-central-1.aws',
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
        st.write("Aucune évaluation trouvée pour le cours avec l'ID spécifié.")
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

def notes2Etudiant(idEt):
    conn = connectSno()
    cursor = conn.cursor()
    query = f"""
        SELECT DISTINCT C.TitreDuCours, E.EvaluationID, E.TitreDeLEvaluation, N.Note
        FROM Cours C
        INNER JOIN Evaluations E ON C.CoursID = E.COURSID
        LEFT JOIN Notes N ON N.EtudiantID = {idEt} AND N.EvaluationID = E.EvaluationID
        """
    cursor.execute(query)
    result = cursor.fetchall()
    
    if result:
        cours_uniques = set(row[0] for row in result)
        selected_cours = st.selectbox("Sélectionnez un cours", list(cours_uniques))
        filtered_result = [row for row in result if row[0] == selected_cours]
        st.write(f"Voici les notes de l'étudiant pour le cours {selected_cours}:")
        for row in filtered_result:
            st.write(f"Evaluation: {row[2]}, Note: {row[3]}")
    else:
        st.write("Aucune note trouvée pour cet étudiant.")

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

if 'prof_ready' not in st.session_state:
    st.session_state['prof_ready'] = False

if 'etudiant_ready' not in st.session_state:
    st.session_state['etudiant_ready'] = False

logo_image = "logo.png"

st.image(logo_image, use_column_width='auto')

if st.session_state['etudiant_ready'] == True:
    welcome(st.session_state['prenom'], st.session_state['nom'])
    sessions = get_sessions()
    sess = st.selectbox("Sélectionnez une session",[ses[2] for ses in sessions])
    selected_session_id = [session[0] for session in sessions if session[2] == sess][0]
    with st.expander(f"Checker l'horaire"):
        st.write("Pas d informations valides")
    with st.expander(f"Liste des cours"):
        st.write("Pas d informations valides")
    with st.expander(f"Consulter mes notes"):
        notes2Etudiant(st.session_state['id'])


if st.session_state['prof_ready'] == True:
    welcome(st.session_state['prenom'], st.session_state['nom'])
    sessions = get_sessions()
    sess = st.selectbox("Sélectionnez une session",[ses[2] for ses in sessions])
    selected_session_id = [session[0] for session in sessions if session[2] == sess][0]
    with st.expander(f"Liste des cours"):
        cours = get_cours(st.session_state['enseignant_data']['id'],selected_session_id)
        if cours:
            for cour in cours:
                titre = cour[1]
                st.write(f"- {titre}")
                cours_id = cour[0]
                structure_modifiee = cour[5]
                if structure_modifiee:
                    struct = st.markdown(f':red[>> [Modifier la structure de l\'evaluation](http://localhost:8522?page=2&cours_id={cours_id})]')  
                    groupes = get_groups(cours_id)
                    selected_groupe = st.selectbox(">>Sélectionnez un groupe", groupes)
                    
                    afficher_evaluations_par_cours(cours_id,selected_groupe)
                else:
                    struct = st.markdown(f':red[>>[Modifier la structure de l\'evaluation](http://localhost:8522?page=2&cours_id={cours_id})]')

        else:
            st.success("Vous avez pas cours cette session")

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
        
       