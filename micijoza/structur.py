import streamlit as st
import snowflake.connector as sf

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

def update_course(course_id):
    conn = connectSno()
    cursor = conn.cursor()
    update_query = f"UPDATE COURS SET ESTSTRUCTMODIF=TRUE WHERE COURSID ={course_id}"
    try:
        cursor.execute(update_query)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Le cours avec l'ID {course_id} a été mis à jour avec succès.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour du cours : {str(e)}")

def delete_evaluation(cours_id):
    conn = connectSno()
    cursor = conn.cursor()
    delete_query = f"DELETE FROM EVALUATIONS WHERE COURSID = {cours_id}"
    try:
        cursor.execute(delete_query)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"Toutes les évaluations pour le cours avec l'ID {cours_id} ont été supprimées avec succès.")
    except Exception as e:
        print(f"Erreur lors de la suppression des évaluations : {str(e)}")
cacheDeleteCour = st.cache_data(delete_evaluation)

def insert_evaluation(cours_id, nom, ponderation, dblstd):
    conn = connectSno()
    cursor = conn.cursor()
    insert_query = f"INSERT INTO EVALUATIONS (COURSID, TITREDELEVALUATION, PONDERATION, DBLSTD) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(insert_query, (cours_id, nom, ponderation, dblstd))
        conn.commit()
        print(f"Évaluation insérée avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'insertion de l'évaluation : {str(e)}")
cacheInsertEva = st.cache_data(insert_evaluation)

def ess(cours_id):
    conn = connectSno()
    cursor = conn.cursor()
    select_query = f"SELECT ESTSTRUCTMODIF FROM COURS WHERE COURSID = {cours_id}"
    cursor.execute(select_query)
    result = cursor.fetchone()
    return result
cacheEssEva = st.cache_data(ess)

def afficher_informations_existantes(cours_id):
    conn = connectSno()
    cursor = conn.cursor()
    select_query = f"SELECT * FROM EVALUATIONS WHERE COURSID = {cours_id}"
    cursor.execute(select_query)
    result = cursor.fetchall()
    if not result:
        st.write("Aucune information existante n'a été trouvée.")
    else:
        st.write("Informations existantes :")
        for row in result:
            row_dict = {
                "NOM": row[1],  # Remplacez les indices par les colonnes appropriées
                "PONDERATION": row[3],
                "DBLSTD": row[5]
            }
            st.write(f"Nom : {row_dict['NOM']}, Pondération : {row_dict['PONDERATION']}, Double Standard : {row_dict['DBLSTD']}")
           
    cursor.close()
    conn.close()
cacheEva = st.cache_data(afficher_informations_existantes)

st.title("Gestion de la Structure de l'Évaluation")
st.write("Informations sur les évaluations")
query_params = st.experimental_get_query_params()
cours_id = query_params.get("cours_id", [None])[0]
noms_evaluations = []
ponderations_evaluations = []
cases_cocher = []
res = ess(cours_id)
if res:
    afficher_informations_existantes(cours_id)
nbre = st.number_input("Veuillez saisir le nombre totales des évaluations", value=1, min_value=1)
for i in range(nbre):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        nom = st.text_input(f"Nom", "", key=f"nom_{i}")
    with col2:
        ponderation = st.number_input(f"Pondération", value=0, min_value=0, max_value=100, key=f"pond_{i}")
    with col3:
        st.markdown("<span style='font-size: 13px;'>Double Standard</span>", unsafe_allow_html=True)
        case_cocher = st.checkbox(f"activate ", key=f"coch_{i}")
    noms_evaluations.append(nom)
    ponderations_evaluations.append(ponderation)
    cases_cocher.append(case_cocher)
modifier = st.button("Modifier")
if modifier:
    for i, nom in enumerate(noms_evaluations):
        totPond = sum(ponderations_evaluations)
    if not nom:
        st.error(f"Le nom de l'évaluation {i+1} est vide.")
    elif totPond != 100:   
        st.warning(f"La somme des pondérations est de {totPond}%, elle doit être égale à 100%.")
    else:
        if cours_id:
            if res:
                delete_evaluation(cours_id)
                for i, nom in enumerate(noms_evaluations):
                    insert_evaluation(cours_id, nom, ponderations_evaluations[i], cases_cocher[i])
                update_course(cours_id)
                st.success('Done')
            else:
                for i, nom in enumerate(noms_evaluations):
                    insert_evaluation(cours_id, nom, ponderations_evaluations[i], cases_cocher[i])
                update_course(cours_id)
                st.success('Done')
        else:
            st.write("ha howa")

    

