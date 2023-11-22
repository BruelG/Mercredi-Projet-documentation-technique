# confirmation_email/email_functions.py
from email.message import EmailMessage
import ssl
import smtplib
import uuid

def send_confirmation_email(author_email, first_name):
    confirmation_code = str(uuid.uuid4())[:8].upper()
    confirmation_message = f"""
            Dear {first_name},

            Thank you for submitting your contribution 
            with our platform. We are pleased to confirm 
            your registration.

            Your confirmation code is: {confirmation_code}

            Please enter this code to verify your email
            address and complete the registration process.

            If you have any questions or need further
            assistance, feel free to contact our support team.

            Best regards,
            Publish
            """

    msg = EmailMessage()
    msg.set_content(confirmation_message)
    msg["Subject"] = "IRIA Congress 2023 Contribution Submission Confirmation"
    msg["From"] = "publishour@gmail.com"  # Remplacez par votre adresse e-mail
    msg["To"] = author_email

    # Configuration du serveur SMTP (Gmail dans cet exemple)
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    smtp_username = "publishour@gmail.com"  # Remplacez par votre adresse e-mail Gmail
    smtp_password = "yoyi onqp eopn rcpu"  # Remplacez par votre mot de passe Gmail
    context = ssl.create_default_context()

    # Envoi de l'e-mail
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

    return confirmation_code
