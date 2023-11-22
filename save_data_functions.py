import json
import snowflake.connector
import streamlit as st
# Connexion à Snowflake (remplacez les valeurs par vos informations d'identification)
conn = snowflake.connector.connect(
    user='christiane',
    password='Kkcv2002@gkmm',
    account='rwwrqgg-fb48745',
    warehouse='COMPUTE_WH',
    database='RCWPROJET',
    schema='CHRISTIANE'
)

# Fonction pour sauvegarder les données dans Snowflake
def save_to_snowflake(query, data):
    cursor = conn.cursor()

    try:
        # Exécutez la requête avec les données
        cursor.execute(query, data)
        conn.commit()
    finally:
        cursor.close()

# Fonction pour sauvegarder les données de contribution dans Snowflake
def save_contribution_data_snowflake(contribution_title, track_preference, main_topic, contribution_type, abstract, content_type, cher_email, code_confirmation):

    try:
        
        cursor = conn.cursor()
        insert_query = "INSERT INTO CONTRIBUTION (CONTRIBUTION_TITLE, TRACK_PREFERENCE, MAIN_TOPIC, CONTRIBUTION_TYPE, ABSTRACT, CONTENT_TYPE, CHER_EMAIL, CODE_CONFIRMATION) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (contribution_title, track_preference, main_topic, contribution_type, abstract, content_type, cher_email, code_confirmation))
        conn.commit()
        st.success(f"Your contribution {contribution_title}  has been saved in the database.")
    except Exception as e:
        st.error(f"An error occurred while saving the contribution: {str(e)}")
    finally:
        conn.close()
