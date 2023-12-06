# registration_functions.py
import snowflake.connector
import streamlit as st

def save_payment_info(payment_method, card_number, expiration_date, cvv):
    # Mise à jour des informations de connexion (idéalement, utilisez des variables d'environnement pour stocker ces valeurs)
    snowflake_config = {
        "user": "christiane",
        "password": "Kkcv2002@gkmm",  # Replace with your password
        "account": "rwwrqgg-fb48745",
        "warehouse": "COMPUTE_WH",
        "database": "RCWPROJET",
        "schema": "CHRISTIANE"  # Use the "registration" schema for registration data
    }
    try:
        conn = snowflake.connector.connect(**snowflake_config)
        cursor = conn.cursor()
        insert_query = "INSERT INTO payment_info (payment_method, card_number, expiration_date, cvv) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (payment_method, card_number, expiration_date, cvv))
        conn.commit()
        st.success(f"Your {payment_method} payment has been processed and saved in the database.")
    except Exception as e:
        st.error(f"An error occurred while processing the payment: {str(e)}")
    finally:
        conn.close()
def save_registration_info(confirmation_code, selected_registration, extra_pages, extra_gala_dinners):
    # Define Snowflake connection parameters
    snowflake_config = {
        "user": "christiane",
        "password": "Kkcv2002@gkmm",  # Replace with your password
        "account": "rwwrqgg-fb48745",
        "warehouse": "COMPUTE_WH",
        "database": "RCWPROJET",
        "schema": "CHRISTIANE"  # Use the "registration" schema for registration data
    }

    try:
        conn = snowflake.connector.connect(**snowflake_config)
        cursor = conn.cursor()
        
        # Define the INSERT query for the registration table
        insert_query = "INSERT INTO registration (confirmation_code, selected_registration, extra_pages, extra_gala_dinners) VALUES (%s, %s, %s, %s)"

        # Execute the INSERT query with the provided data
        cursor.execute(insert_query, (confirmation_code, selected_registration, extra_pages, extra_gala_dinners))
        conn.commit()
        st.success("Your registration information has been saved in the database.")
    except Exception as e:
        st.error(f"An error occurred while processing the registration: {str(e)}")
    finally:
        conn.close()

def confirm_email(confirmation_code, email):
    snowflake_config = {
        "user": "christiane",
        "password": "Kkcv2002@gkmm",
        "account": "rwwrqgg-fb48745",
        "warehouse": "COMPUTE_WH",
        "database": "RCWPROJET",
        "schema": "CHRISTIANE"
    }

    try:
        conn = snowflake.connector.connect(**snowflake_config)
        cursor = conn.cursor()

        query = "SELECT * FROM RCWPROJET.CHRISTIANE.CONTRIBUTION WHERE CODE_CONFIRMATION = %s AND CHER_EMAIL = %s"
        cursor.execute(query, (confirmation_code, email))
        result = cursor.fetchone()

        if result:
            st.success("Confirmation de l'email réussie. Vous êtes maintenant inscrit.")
        else:
            st.error("Code de confirmation ou email invalide. Veuillez réessayer.")
    except Exception as e:
        st.error(f"Une erreur s'est produite lors de la confirmation de l'email : {str(e)}")
    finally:
        conn.close()


def save_to_database(email, title, first_name, last_name, institution, country,
                      street_address, city, state, postal_code, phone, fax, vat, about_conference):
     # Mise à jour des informations de connexion (idéalement, utilisez des variables d'environnement pour stocker ces valeurs)
    snowflake_config = {
        "user": "christiane",
        "password": "Kkcv2002@gkmm",  # Replace with your password
        "account": "rwwrqgg-fb48745",
        "warehouse": "COMPUTE_WH",
        "database": "RCWPROJET",
        "schema": "CHRISTIANE"  # Use the "registration" schema for registration data
    }
    try:
        # Établir une connexion à Snowflake
        conn = snowflake.connector.connect(**snowflake_config)
        cursor = conn.cursor()

        # Définir la requête INSERT pour la table chercheur
        insert_query = '''
            INSERT INTO CHERCHEUR (
                EMAIL, TITLE, FIRST_NAME, LAST_NAME, INSTITUTION, COUNTRY, STREET_ADDRESS,
                CITY, STATE, POSTAL_CODE, PHONE, FAX, VAT, ABOUT_CONFERENCE
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        # Exécuter la requête INSERT avec les données fournies
        cursor.execute(insert_query, (
            email, title, first_name, last_name, institution, country,
            street_address, city, state, postal_code, phone, fax, vat, about_conference
        ))

        # Valider les changements dans la base de données
        conn.commit()

        # Afficher un message de succès à l'utilisateur
        st.success("Votre information de chercheur a été enregistrée dans la base de données.")
    except Exception as e:
        # Afficher un message d'erreur en cas d'exception
        st.error(f"Une erreur s'est produite lors du traitement de l'enregistrement : {str(e)}")
    finally:
        # Fermer la connexion à Snowflake dans le bloc finally
        conn.close()