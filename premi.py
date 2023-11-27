import pandas as pd
import streamlit as st
import snowflake.connector

snowflake_config = {
        'user': 'MICIJOZAA',
        'password': '!0Micijoza',
        'account': 'ul81046.ca-central-1.aws',
        'warehouse': 'COMPUTE_WH',
        'database': 'DOCUMENTATION',
        'schema': 'MICIJOZA'
}
def verifier_informations(num_enseignant, nas):
    try:
        conn = snowflake.connector.connect(**snowflake_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ENSEIGNANTS WHERE NUMEROPROF = %s AND NAS = %s", (num_enseignant, nas))
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
def mettre_a_jour_mot_de_passe(num_enseignant, nouveau_mot_de_passe):
    try:
        conn = snowflake.connector.connect(**snowflake_config)
        cursor = conn.cursor()

        cursor.execute("UPDATE ENSEIGNANTS SET MOTDEPASSE = %s WHERE NUMEROPROF = %s", (nouveau_mot_de_passe, num_enseignant))
        conn.commit()

    except Exception as e:
        print(f"Erreur lors de la mise à jour du mot de passe : {str(e)}")

    finally:
        conn.close()

mettre_a_jour_mot_de_passe = st.cache_data(mettre_a_jour_mot_de_passe)
logo_image = "logo.png"
st.image(logo_image)
st.header("Première utilisation \n Saisie d'informations personnelles")

st.header(" ")
st.write('<span style="color: #DECC80; font-weight: bold; font-family: cursive;">Pour utiliser le système, vous devez vous servir de votre Code d\'utilisateur. Ce numéro apparaît généralement sur vos bordereaux de paie.</span>', unsafe_allow_html=True)
st.write('<span style="color: #DECC80; font-weight: bold; font-family: cursive;">Pour accéder à m i c i j o z a, vous devrez vous choisir un mot de passe à l\'aide de cette page. Une fois votre mot de passe en main, vous pourrez l\'utiliser pour vos prochaines visites.</span>', unsafe_allow_html=True)
st.write('<span style="color: #DECC80; font-weight: bold; font-family: cursive;">Afin de vous identifier, veuillez entrer les informations personnelles afin qu\'Omnivox puisse vous identifier. Toute tentative d\'accès avec des données qui ne sont pas les vôtres constitue un usage frauduleux passible d\'actions légales ainsi que de sanctions sévères.</span>', unsafe_allow_html=True)
st.markdown("<h2 style='color: #8D622B;'>Saisie d'informations personnelles</h2>", unsafe_allow_html=True)
num_enseignant = st.text_input("Code d'utilisateur")
nas = st.text_input("6 derniers chiffres du NAS")
est_robot = st.checkbox("Je ne suis pas un robot")
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    valider = st.checkbox("Valider")
if valider and est_robot:
    true =verifier_informations(num_enseignant, nas)
    if true:
        nouveau_mot_de_passe = st.text_input("Nouveau mot de passe", type="password")
        confirmer_mot_de_passe = st.text_input("Confirmer le mot de passe", type="password")
        if st.button("Modifier"):
            if nouveau_mot_de_passe == confirmer_mot_de_passe:
                mettre_a_jour_mot_de_passe(num_enseignant, nouveau_mot_de_passe)
                st.success("Mot de passe mis à jour avec succès.")
            else:
                st.error("La confirmation du mot de passe ne correspond pas.")
    else:
        st.error("Les informations sont incorrectes. Veuillez réessayer.")
elif valider and not est_robot:
    st.error("Veuillez saisir vos infos et prouver que vous etes pas un robot!")
