import streamlit as st
import pickle
import time

# Demaragge avec l'environnement myenv


model = pickle.load(open('svm_model.pkl', 'rb'))


st.title('Helsinki :space_invader:')
st.write('Prédiction Fictif Au passage ou A L\'Echec de cours Basee sur des donnees Historiques')
st.sidebar.header('Paramètres')






sexe_options = {"Femme": 0, "Homme": 1}
etat_matrimonial_options = {"Célibataire": 0, "En couple": 1}
provenance_options = {"Afrique": 0, "Europe": 1, "Asie": 2, "Oceanie": 3, "Amerique": 4}


cours = [
    "Programmation orientée objet", "Application mobile 1", "Application mobile 2",
    "Intelligence artificielle 1", "Intelligence artificielle 2", "Structure de base de données",
    "Français 1", "Français 2", "Français 3", "Philosophie 1", "Philosophie 2", "Philosophie 3",
    "Anglais", "Espagnol", "Périphériques et objets connectés",
    "Mathématiques discrètes", "Systèmes d'exploitation", "Réseaux informatiques",
    "Conception de bases de données", "Algorithmes avancés", "Développement web avancé",
    "Sécurité informatique", "Langages de programmation avancés", "Machine Learning",
    "Traitement du langage naturel", "Intelligence artificielle éthique", "Robotique",
    "Génie logiciel", "Big Data Analytics"
]


sexe = st.sidebar.radio('Sexe', list(sexe_options.keys()))
age = st.sidebar.number_input('Âge', min_value=17, max_value=40)
nom_cours = st.sidebar.selectbox('Nom du cours', cours)
distance_parcourus_KM = st.sidebar.number_input('Distance parcourue (KM)', min_value=1, max_value=30)
nombre_heure_retard = st.sidebar.number_input('Nombre d\'heures de retard', min_value=0, max_value=25)
travail = st.sidebar.radio('Travail', ["Oui", "Non"])
premiere_fois = st.sidebar.radio('Première fois', ["Oui", "Non"])
nb_heure_travail_semaine = st.sidebar.number_input('Nombre d\'heures de travail par semaine', min_value=0, max_value=35)
Tutorat = st.sidebar.radio('Tutorat', ["Oui", "Non"])
provenance = st.sidebar.selectbox('Provenance', list(provenance_options.keys()))
vehicule = st.sidebar.radio('Véhicule', ["Oui", "Non"])
vis_seul = st.sidebar.radio('Vit seul', ["Oui", "Non"])
etat_matrimonial = st.sidebar.radio('État matrimonial', list(etat_matrimonial_options.keys()))
heure_moyenne_sommeil = st.sidebar.number_input('Heure moyenne de sommeil', min_value=4, max_value=10)


# if travail == "Oui":
#     nb_heure_travail_semaine = st.sidebar.number_input('Nombre d\'heures de travail par semaine', min_value=1, max_value=100)
# else:
#     nb_heure_travail_semaine = 0

# if Tutorat == "Oui":
#     cours_tutorat = st.sidebar.selectbox('Cours de tutorat', cours)
# else:
#     cours_tutorat = ""

travail_value = 1 if travail == "Oui" else 0
premiere_fois_value = 1 if premiere_fois == "Oui" else 0
Tutorat_value = 1 if Tutorat == "Oui" else 0
vehicule_value = 1 if vehicule == "Oui" else 0
vis_seul_value = 1 if vis_seul == "Oui" else 0

if st.sidebar.button('Prédire la classe'):
    with st.spinner('Prédiction en cours...'):
        st.snow()
        time.sleep(1)  
        features = [
            sexe_options[sexe],
            age,
            distance_parcourus_KM,
            nombre_heure_retard,
            travail_value,
            premiere_fois_value,
            nb_heure_travail_semaine,
            Tutorat_value,
            provenance_options[provenance],
            vehicule_value,
            vis_seul_value,
            etat_matrimonial_options[etat_matrimonial],
            heure_moyenne_sommeil
        ]
        prediction = model.predict([features])
        print(prediction)
    
    st.write('## Résultat de la prédiction')
    st.write(prediction)
    if prediction[0] == 0:
        st.write(f'Il y a de fortes chances que vous échouiez au cours **"{nom_cours}"** selon notre IA basée sur des données historiques.')  
    else:
        st.write(f'Il y a de fortes chances que vous réussissiez le cours **"{nom_cours}"** selon notre IA basée sur des données historiques.')

# Bouton pour voir les statistiques
# if st.button('Voir statistiques'):
#     # Charger les données
#     df = pd.read_csv('donnees.csv')

#     # Générer un rapport de profil avec pandas profiling
#     profile = ProfileReport(df, title='Pandas Profiling Report')

