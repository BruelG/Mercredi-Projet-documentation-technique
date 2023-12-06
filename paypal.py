import streamlit as st
import paypalrestsdk

# Configure PayPal environment (remplacez les informations par les vôtres)
paypalrestsdk.configure({
    "mode": "sandbox",  # Changez à "live" pour la production
    "client_id": "AedG7hgccoHVoznGOI2ecKeaz1ZAwpWAtWQGVj4txAWrfyYWx4e3bUBzhpIWFJlhWZSqDpirm8lKyxkM",
    "client_secret": "EMb3D4rH8rJNUWm4a0LdCyYZTWYXBf4kKGzue-Q4rZL8rI1adXqJOaG4RUFmuS9Jwq81cJZQRpsIlrvQ"
})

# Fonction pour créer un paiement
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

# Interface utilisateur Streamlit
def main():
    st.title("Soumettre un article - Paiement PayPal")

    # Informations sur l'article
    st.header("Détails de l'article")
    st.subheader("Titre : Article scientifique")
    st.subheader("Prix : 54,00 $ (taxes incluses)")
    st.subheader("Description : Soumettez votre article en effectuant le paiement.")

    # Bouton pour effectuer le paiement
    if st.button("Effectuer le paiement"):
        st.markdown("Redirection vers PayPal...")

        # Créer le paiement
        payment = create_payment()
        if payment:
            approval_url = next(link.href for link in payment.links if link.rel == 'approval_url')
            st.markdown(f"Cliquez [ici]({approval_url}) pour finaliser le paiement.")
        else:
            st.error("Une erreur s'est produite lors de la création du paiement.")

# Exécution de l'application Streamlit
if __name__ == "__main__":
    main()
