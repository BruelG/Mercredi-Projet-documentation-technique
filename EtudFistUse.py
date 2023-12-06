import pandas as pd
import streamlit as st
import snowflake.connector

snowflake_config = {
    'user': 'MICIJOZA',
    'password': '!0Maroua',
    'account': 'er82671.us-east4.gcp',
    'warehouse': 'COMPUTE_WH',
    'database': 'DOCUMENTATION',
    'schema': 'MICIJOZA'
}
def verifier_informations(num, month,day,year,code):
    try:
        conn = snowflake.connector.connect(**snowflake_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ETUDIANTS WHERE CODEPERMANENT = %s AND DATEDENAISSANCE = %s AND NUMERODA = %s" , (code, f'{year}-{month}-{day}', num))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False

    except Exception as e:
        print(f"Erreur lors de la vérification des informations : {str(e)}")
        return False

    finally:
        conn.close()
verifier_informations = st.cache_data(verifier_informations)
def mettre_a_jour_mot_de_passe(code, nouveau_mot_de_passe):
    try:
        conn = snowflake.connector.connect(**snowflake_config)
        cursor = conn.cursor()

        cursor.execute("UPDATE ETUDIANTS SET MOTDEPASSE = %s WHERE CODEPERMANENT = %s", (nouveau_mot_de_passe, code))
        conn.commit()

    except Exception as e:
        print(f"Erreur lors de la mise à jour du mot de passe : {str(e)}")

    finally:
        conn.close()
mettre_a_jour_mot_de_passe = st.cache_data(mettre_a_jour_mot_de_passe)
st.header("Première utilisation \n Saisie d'informations personnelles")

st.header(" ")
st.write('<span style="color: purple; font-weight: bold; font-family: cursive;">Pour utiliser le système, vous devez vous servir de votre Numéro d\'étudiant. Ce numéro apparaît sur la plupart des documents officiels envoyés par le collège ainsi que sur votre carte étudiante.</span>', unsafe_allow_html=True)
st.write('<span style="color: purple; font-weight: bold; font-family: cursive;">Pour accéder à m i c i j o z a, vous devrez vous choisir un mot de passe à l\'aide de cette page. Une fois votre mot de passe en main, vous pourrez l\'utiliser pour vos prochaines visites.</span>', unsafe_allow_html=True)
st.write('<span style="color: purple; font-weight: bold; font-family: cursive;">Afin de vous identifier, veuillez entrer les informations personnelles afin que m i c i j o z a puisse vous identifier. Toute tentative d\'accès avec des données qui ne sont pas les vôtres constitue un usage frauduleux passible d\'actions légales ainsi que de sanctions sévères incluant le renvoi du Collège</span>', unsafe_allow_html=True)
st.markdown("<h2 style='color: pink;'>Saisie d'informations personnelles</h2>", unsafe_allow_html=True)
num = st.text_input("Numéro d'étudiant (7 derniers chiffres)")
code = st.text_input("Code permanent")
st.write("Date de naissance")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    month = st.selectbox("Mois", list(range(1, 13)))
with col2:
    if month in [1, 3, 5, 7, 8, 10, 12]:
        day = st.selectbox("Jour", list(range(1, 32)))
    elif month in [4, 6, 9, 11]:
        day = st.selectbox("Jour", list(range(1, 31)))
    else:
        day = st.selectbox("Jour", list(range(1, 29)))
with col3:
    year = st.selectbox("Année", list(range(1924, 2024)))
est_robot = st.checkbox("Je ne suis pas un robot")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    valider = st.checkbox("Valider")
if valider and est_robot:
    true =verifier_informations(num, month,day,year,code)
    if true:
        nouveau_mot_de_passe = st.text_input("Nouveau mot de passe", type="password")
        confirmer_mot_de_passe = st.text_input("Confirmer le mot de passe", type="password")
        if st.button("Modifier"):
            if nouveau_mot_de_passe == confirmer_mot_de_passe:
                mettre_a_jour_mot_de_passe(code, nouveau_mot_de_passe)
                st.success("Mot de passe mis à jour avec succès.")
            else:
                st.error("La confirmation du mot de passe ne correspond pas.")
    else:
        st.error("Les informations sont incorrectes. Veuillez réessayer.")
elif valider and not est_robot:
    st.error("Veuillez saisir vos infos et prouver que vous etes pas un robot!")
