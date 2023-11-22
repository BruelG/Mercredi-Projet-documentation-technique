import streamlit as st
from contribution.contribution_functions import submit_contribution, submit_contribution_author, submit_additional_authors, g_main_topics,show_submitted_informations
#from save_data.save_data_functions import save_contribution_data, show_submitted_information
from confirmation_email.email_functions import send_confirmation_email
from save_data.save_data_functions import save_contribution_data_snowflake
from contribution.registration_functions import save_payment_info, save_registration_info, confirm_email,save_to_database
import re

# Fonction pour la page d'inscription

def show_inscription_page():
    # Définir la réponse au défi "To prove you are not a robot"
    challenge_response = "13"  # La réponse correcte est "13"

    # Définir un titre pour votre application Streamlit
    st.title("IARIA Congress 2023 - Submit a New Contribution")

    # Créer le formulaire de soumission
    contribution_title, track_preference, main_topic, contribution_type, content_type, challenge_answer = submit_contribution()

    # Formulaire pour l'auteur principal
    st.subheader("Author Information (Contact Author):")
    contact_author, author_email, first_name, last_name, institution, country = submit_contribution_author()

    # Définir le motif pour vérifier le format de l'e-mail
    email_pattern = r'^[\w\.-]+@[\w\.-]+(\.\w+)+$'

    # Liste pour les autres auteurs
    st.subheader("Additional Authors:")
    num_additional_authors, additional_authors = submit_additional_authors()

    # Champ pour l'abstract
    abstract = st.text_area("Abstract")

    # Liste des topics
    st.subheader("Topics")
    main_topic_options = g_main_topics()
    selected_topics = st.multiselect("Select Topics", main_topic_options)
    confirmation_code = send_confirmation_email(author_email, first_name)
    # Boutons Submit et Reset
    if st.button("Submit Contribution"):
        if (
            contribution_title
            and track_preference
            and main_topic
            and contribution_type
            and content_type
            and challenge_answer == challenge_response
            and first_name
            and last_name
            and institution
            and re.match(email_pattern, author_email)  # Vérification de l'e-mail de l'auteur principal
        ):
            try:
                # Enregistrez les données de la contribution dans la base de données ou un autre système de stockage
                save_contribution_data_snowflake(contribution_title, track_preference, main_topic, contribution_type, abstract, content_type,author_email, confirmation_code)

                # Affichez les informations soumises en bas de la page
                show_submitted_informations(contribution_title, track_preference, main_topic, contribution_type, content_type,
                                            author_email, first_name, last_name, institution, country,
                                            additional_authors, abstract, selected_topics)

                # Envoyez l'e-mail de confirmation
                send_confirmation_email(author_email, first_name)

                st.success(f"Contribution '{contribution_title}' submitted successfully.")
                st.info("Please check your email for further instructions.")
            except Exception as e:
                st.error(f"An error occurred while processing the contribution: {str(e)}")
        else:
            st.error("Please fill in all required fields and pass the challenge.")

    # Bouton Reset
    if st.button("Reset"):
        st.experimental_rerun()

# Fonction pour la page d'inscription
import streamlit as st

def show_registration_page():
    st.title("Registration and Payment")
    st.title("Registration Form")

    # Formulaire d'inscription
    email = st.text_input("Email")
    title = st.text_input("Title")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    institution = st.text_input("Institution")
    country = st.text_input("Country")
    street_address = st.text_input("Street Address")
    city = st.text_input("City")
    state = st.text_input("State")
    postal_code = st.text_input("Postal Code")
    phone = st.text_input("Phone")
    fax = st.text_input("Fax")
    vat = st.text_input("VAT")
    about_conference = st.text_area("About Conference")

    # Bouton de soumission du formulaire
    if st.button("Submit"):
        save_to_database(email, title, first_name, last_name, institution, country,
                          street_address, city, state, postal_code, phone, fax, vat, about_conference)
        st.success("Registration submitted successfully!")
    # Section de confirmation de l'email0000
    st.header("Email Confirmation")

    # Entrée du code de confirmation
    confirmation_code_input = st.text_input("Enter Confirmation Code")
    email_input = st.text_input("Enter Email for Confirmation")

    # Bouton de confirmation
    if st.button("Confirm Email"):
        confirm_email(confirmation_code_input, email_input)

    # Section d'inscription
    st.header("Registration")

    selected_registration = st.selectbox(
        "Select Registration",
        [
            "Select Registration",
            "Registration iaria fellow - 645 EUR",
            "Registration Full time student - 645 EUR",
            "Registration Academic - 695 EUR",
            "Registration Industry - 835 EUR"
        ]
    )

    # Section d'options supplémentaires
    st.header("Additional Options")
    extra_pages = st.selectbox("Extra Pages (105 EUR per page over 6 pages)", list(range(7)), format_func=lambda x: 'No extra pages' if x == 0 else f"{x} extra pages")
    extra_gala_dinners = st.selectbox("Extra Gala Dinners (95 EUR, needed for accompanying persons)", list(range(4)), format_func=lambda x: 'No extra dinners' if x == 0 else f"{x} extra dinner(s)")

    # Bouton d'inscription
    if st.button("Submit Registration"):
        save_registration_info(confirmation_code_input, selected_registration, extra_pages, extra_gala_dinners)

    # Section de paiement
    st.title("Payment")

    # Sélection du mode de paiement
    payment_method = st.radio("Select Payment Method", ["Visa", "MasterCard", "Discover", "American Express", "Bank Transfer"])

    if payment_method != "Bank Transfer":
        st.subheader("Card Details")
        card_number = st.text_input("Card Number")
        expiration_date = st.text_input("Expiration Date (MM/YY)")
        cvv = st.text_input("CVV")

    # Bouton de paiement
    if st.button("Submit Payment"):
        if payment_method == "Bank Transfer":
            st.success("Your bank transfer has been processed.")
        else:
            save_payment_info(payment_method, card_number, expiration_date, cvv)

# Note: Assurez-vous d'avoir les fonctions confirm_email, save_registration_info, et save_payment_info définies dans votre code.

# Fonction principale
def main():
    # Titre de l'application
    st.title("ACADEMIC PUBLISH")

    # Titre de la barre latérale
    st.sidebar.title("CHOOSE YOUR PAGE")

    # Liste déroulante pour la navigation sur la gauche
    selected_page = st.sidebar.selectbox("", ["Home", "SUBMIT A CONTRIBUTION", "REGISTER"])

    # Afficher le contenu en fonction de la page sélectionnée
    if selected_page == "Home":
        st.write("WELCOME TO YOUR PLATFORM TO SUBMIT YOUR SCIENTIFIC ARTICLE")
    elif selected_page == "SUBMIT A CONTRIBUTION":
        show_inscription_page()
    elif selected_page == "REGISTER":
        show_registration_page()


# Exécutez l'application
if __name__ == "__main__":
    main()
