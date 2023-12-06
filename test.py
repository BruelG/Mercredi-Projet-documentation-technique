# contribution_functions.py

# Remplacez cette importation par les modules nécessaires pour votre logique
# par exemple, pour PayPal, vous pourriez utiliser une bibliothèque comme `paypalrestsdk`
# pour Snowflake, vous pourriez utiliser `snowflake.connector`
import paypalrestsdk
import snowflake.connector

# Définir les informations de connexion pour Snowflake
snowflake_user = "votre_utilisateur_snowflake"
snowflake_password = "votre_mot_de_passe_snowflake"
snowflake_account = "votre_compte_snowflake"
snowflake_database = "votre_base_de_donnees_snowflake"
snowflake_schema = "votre_schema_snowflake"

# Initialiser la configuration PayPal
paypalrestsdk.configure({
    "mode": "sandbox",  # Changez à "live" pour la production
    "client_id": "AedG7hgccoHVoznGOI2ecKeaz1ZAwpWAtWQGVj4txAWrfyYWx4e3bUBzhpIWFJlhWZSqDpirm8lKyxkM",
    "client_secret": "EMb3D4rH8rJNUWm4a0LdCyYZTWYXBf4kKGzue-Q4rZL8rI1adXqJOaG4RUFmuS9Jwq81cJZQRpsIlrvQ"
})


# Fonction pour créer un paiement PayPal
def create_payment():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": "http://localhost:8501/",  # Remplacez par votre URL de succès
            "cancel_url": "http://localhost:8501/"    # Remplacez par votre URL d'annulation
        },
        "transactions": [{
            "amount": {
                "total": "54.00",  # Montant total du paiement
                "currency": "CAD"
            },
            "description": "Paiement pour soumission d'article scientifique"
        }]
    })


    if payment.create():
        return payment
    else:
        return None

# Fonction pour calculer le prix total
def calculate_total_price(selected_registration, extra_pages, extra_gala_dinners):
    # Logique pour calculer le prix total en fonction des options sélectionnées
    # Replacez cela par votre propre logique
    base_price = 54.00  # Prix de base de l'article scientifique
    extra_pages_price = extra_pages * 105.00
    extra_gala_dinners_price = extra_gala_dinners * 95.00

    total_price = base_price + extra_pages_price + extra_gala_dinners_price
    return total_price

# Fonction pour enregistrer les informations d'inscription dans Snowflake
def save_registration_info(confirmation_code, selected_registration, extra_pages, extra_gala_dinners, total_price):
    try:
        con = snowflake.connector.connect(
            user=snowflake_user,
            password=snowflake_password,
            account=snowflake_account,
            warehouse='COMPUTE_WH',
            database=snowflake_database,
            schema=snowflake_schema
        )

        cursor = con.cursor()

        # Exécution de l'insertion dans Snowflake
        cursor.execute("""
            INSERT INTO RCWPROJET.CHRISTIANE.REGISTRATION
            (CONFIRMATION_CODE, SELECTED_REGISTRATION, EXTRA_PAGES, EXTRA_GALA_DINNERS, TOTAL_PRICE)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            confirmation_code,
            selected_registration,
            extra_pages,
            extra_gala_dinners,
            total_price
        ))

        con.commit()

        cursor.close()
        con.close()

        st.success("Your registration information has been successfully saved.")
    except snowflake.connector.errors.Error as error:
        st.error(f"An error occurred while saving registration information: {error}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
