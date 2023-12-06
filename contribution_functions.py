# contribution_functions.py

import streamlit as st
from email.message import EmailMessage
import ssl
import smtplib
import uuid  # Pour générer un UUID unique
import re

# Liste des préférences de piste, des sujets principaux et des types de contribution
track_preferences = ["Academic Pubish 2023- General event track"]
main_topics = ["Academic Pubish 2023 :Cloud", "Academic Pubish 2023 :Data", "Academic Pubish 2023 :Energy",
               "Academic Pubish :Health", "Academic Pubish 2023 :Human-Machine", "Academic Pubish 2023 :Intelligence",
               "Academic Pubish 2023 :Internet", "Academic Pubish 2023 :IoT", "Academic Pubish 2023 :Learning",
               "Academic Pubish 2023 :Meta verse", "Academic Pubish 2023 :Mobility", "Academic Pubish 2023 :Multimedia"]
contribution_types = ["regular paper", "short paper", "idea"]
content_types = ["academic research", "industry report", "industry research"]

# Liste des pays
countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda",
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas",
    "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin",
    "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei",
    "Bulgaria", "Burkina Faso", "Burundi", "Côte d'Ivoire", "Cabo Verde", "Cambodia",
    "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China",
    "Colombia", "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba",
    "Cyprus", "Czechia (Czech Republic)", "Democratic Republic of the Congo (Congo-Kinshasa)",
    "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt",
    "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia",
    "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana",
    "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti",
    "Holy See", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran",
    "Iraq", "Ireland", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan",
    "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon",
    "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar",
    "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania",
    "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro",
    "Morocco", "Mozambique", "Myanmar (formerly Burma)", "Namibia", "Nauru", "Nepal",
    "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea",
    "North Macedonia (formerly Macedonia)", "Norway", "Oman", "Pakistan", "Palau",
    "Palestine State", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines",
    "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
    "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
    "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia",
    "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan",
    "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan",
    "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia",
    "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom",
    "United States of America", "Uruguay", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam",
    "Yemen", "Zambia", "Zimbabwe"]  # Liste complète des pays

# Fonction pour soumettre la contribution
def submit_contribution():
    contribution_title = st.text_input("Contribution Title")
    track_preference = st.selectbox("Track Preference", track_preferences)
    main_topic = st.selectbox("Main Topic", main_topics)
    contribution_type = st.selectbox("Contribution Type", contribution_types)
    content_type = st.selectbox("Content Type", content_types)
    challenge_answer = st.text_input("To prove you are not a robot, solve 8+5 =", type="password")

    return contribution_title, track_preference, main_topic, contribution_type, content_type, challenge_answer

# Fonction pour soumettre les informations de l'auteur principal
def submit_contribution_author():
    contact_author = st.radio("Is Contact Author?", ["Yes", "No"])
    email_pattern = r'^[\w\.-]+@[\w\.-]+(\.\w+)+$'
    author_email = st.text_input("Email")
    if not re.match(email_pattern, author_email):
        st.error("Invalid email format. Please enter a valid email.")

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    institution = st.text_input("Institution")
    country = st.selectbox("Country", countries)

    return contact_author, author_email, first_name, last_name, institution, country

# Fonction pour soumettre les informations supplémentaires des auteurs
def submit_additional_authors():
    num_additional_authors = st.number_input("Number of Additional Authors", min_value=0, max_value=5)
    additional_authors = []

    for i in range(num_additional_authors):
        st.subheader(f"Author {i + 1}:")
        
        # Provide unique keys for st.radio and st.text_input instances
        contact_author = st.radio(f"Is Contact Author? (Author{i+1})", ["Yes", "No"])
        
        email_pattern = r'^[\w\.-]+@[\w\.-]+(\.\w+)+$'
        author_email= st.text_input(f"Email (Author {i + 1})")
        if not re.match(email_pattern, author_email):
           st.error("Invalid email format. Please enter a valid email.")

        first_name = st.text_input(f"First Name (Author{i+1})", value="")
        last_name = st.text_input(f"Last Name (Author{i+1})", value="")
        institution = st.text_input(f"Institution (Author{i+1})", value="")
        country = st.selectbox(f"Country (Author{i+1})", countries)

        # Append the author information to the list
        additional_authors.append({
            "contact_author": contact_author,
            "author_email": author_email ,
            "first_name": first_name,
            "last_name": last_name,
            "institution": institution,
            "country": country
        })

    return num_additional_authors, additional_authors

def g_main_topics():
    main_topics = [
        "IRIA Congress 2023 :Cloud",
        "IRIA Congress 2023 :Data",
        "IRIA Congress 2023 :Energy",
        "IRIA Congress 2023 :Health",
        "IRIA Congress 2023 :Human-Machine",
        "IRIA Congress 2023 :Intelligence",
        "IRIA Congress 2023 :Internet",
        "IRIA Congress 2023 :IoT",
        "IRIA Congress 2023 :Learning",
        "IRIA Congress 2023 :Meta verse",
        "IRIA Congress 2023 :Mobility",
        "IRIA Congress 2023 :Multimedia"
    ]
    return main_topics
def show_submitted_informations(contribution_title, track_preference, main_topic, contribution_type, content_type,
                               author_email, first_name, last_name, institution, country,
                               additional_authors, abstract):
    st.subheader("Submitted Information:")
    st.write(f"Contribution Title: {contribution_title}")
    st.write(f"Track Preference: {track_preference}")
    st.write(f"Main Topic: {main_topic}")
    st.write(f"Contribution Type: {contribution_type}")
    st.write(f"Content Type: {content_type}")
    st.write(f"Author Email: {author_email}")
    st.write(f"First Name: {first_name}")
    st.write(f"Last Name: {last_name}")
    st.write(f"Institution: {institution}")
    st.write(f"Country: {country}")

    st.subheader("Additional Authors:")
    for i, author in enumerate(additional_authors):
        st.write(f"Additional Author {i + 1}:")
        st.write(f"  - First Name: {author['first_name']}")
        st.write(f"  - Last Name: {author['last_name']}")
        st.write(f"  - Email: {author['author_email']}")

    st.write(f"Abstract: {abstract}")
    #st.write(f"Selected Topics: {', '.join(selected_topics)}")

##registration

