import streamlit as st
import snowflake.connector
from contribution_functions import submit_contribution, submit_contribution_author, submit_additional_authors, show_submitted_informations

# Remplacez ces valeurs par vos propres informations de connexion à Snowflake
snowflake_user = "christiane"
snowflake_password = "Kkcv2002@gkmm"
snowflake_account = "rwwrqgg-fb48745"
snowflake_database = "RCWPROJET"
snowflake_schema = "CHRISTIANE"

def modify_information():
    # ... (code précédent inchangé)

    # Bouton pour soumettre la modification
    if st.button("Submit Modification"):
        try:
            # Connexion à Snowflake
            con = snowflake.connector.connect(
                user=snowflake_user,
                password=snowflake_password,
                account=snowflake_account,
                warehouse='COMPUTE_WH',
                database=snowflake_database,
                schema=snowflake_schema
            )

            # Création d'un curseur
            cursor = con.cursor()

            # Exécution de la mise à jour dans Snowflake
            cursor.execute("""
                UPDATE RCWPROJET.CHRISTIANE.CONTRIBUTION
                SET
                    CONTRIBUTION_TITLE = %s,
                    TRACK_PREFERENCE = %s,
                    MAIN_TOPIC = %s,
                    CONTRIBUTION_TYPE = %s,
                    ABSTRACT = %s,
                    CONTENT_TYPE = %s,
                    CHER_EMAIL = %s,
                    CODE_CONFIRMATION = %s
                WHERE CONTRIBUTION_ID = %s
            """, (
                contribution_title,
                track_preference,
                main_topic,
                contribution_type,
                abstract,
                content_type,
                author_email,
                confirmation_code,
                contribution_id
            ))

            # Valider les changements dans Snowflake
            con.commit()

            # Fermer le curseur et la connexion
            cursor.close()
            con.close()

            st.success("Your information has been successfully modified.")
        except snowflake.connector.errors.Error as error:
            st.error(f"An error occurred while updating the contribution: {error}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")