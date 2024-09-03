import json
import smtplib
from email.message import EmailMessage
import mimetypes
import logging
from datetime import datetime
import yfinance as yf

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_email_config(config_path: str):
    """
    Charge la configuration de l'email à partir d'un fichier JSON.
    """
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
        logging.info("Configuration de l'email chargée avec succès.")
        return config
    except Exception as e:
        logging.error(f"Erreur lors du chargement de la configuration de l'email : {e}")
        raise

def create_email_message(subject: str, body: str, sender: str, recipients: list, attachment: str):
    """
    Crée un message email avec une pièce jointe.
    """
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg.set_content(body)

        if attachment:
            mime_type, _ = mimetypes.guess_type(attachment)
            maintype, subtype = mime_type.split('/') if mime_type else ('application', 'octet-stream')

            with open(attachment, 'rb') as file:
                msg.add_attachment(file.read(), maintype=maintype, subtype=subtype, filename=file.name)

        logging.info("Message email créé avec succès.")
        return msg
    except Exception as e:
        logging.error(f"Erreur lors de la création du message email : {e}")
        raise

def send_email(msg: EmailMessage, email_config: dict):
    """
    Envoie un message email en utilisant les paramètres SMTP spécifiés dans la configuration.
    """
    try:
        with smtplib.SMTP_SSL(email_config['host'], email_config['port']) as server:
            server.login(email_config['user'], email_config['password'])
            server.send_message(msg)
        logging.info("Email envoyé avec succès.")
    except Exception as e:
        logging.error(f"Echec de l'envoi de l'email : {e}")
        raise

def get_cac40_closing_price():
    """
    Récupère la valeur de clôture actuelle du CAC 40 à partir de Yahoo Finance.
    """
    try:
        ticker = "^FCHI"  # Symbole du CAC 40 sur Yahoo Finance
        data = yf.download(ticker, period="1d", interval="1d")
        closing_price = data['Close'].iloc[-1]  # Récupère la dernière valeur de clôture
        return closing_price
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de la valeur de clôture du CAC 40 : {e}")
        raise

def send_mail(subject: str, body: str, attachment: str = None):
    """
    Envoie un email avec un sujet, un corps de message et une pièce jointe.
    """
    try:
        email_config = load_email_config('./configuration/configMail.json')
        recipients = email_config['to'].split(',')  # Transforme la chaîne des destinataires en liste

        msg = create_email_message(subject, body, email_config['user'], recipients, attachment)
        send_email(msg, email_config)

    except Exception as error:
        logging.error(f"Echec de l'envoi de l'email : {error}")

# Exemple d'utilisation
if __name__ == "__main__":
    # Date actuelle pour personnaliser le sujet et le corps de l'email
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Récupérer la valeur de clôture du CAC 40
    cac40_close_value = get_cac40_closing_price()

    # Sujet de l'email
    subject = f"Résumé Quotidien du Marché - {current_date}"

    # Corps de l'email
    body = f"""
    Bonjour,

    Voici le résumé des activités du marché pour la journée du {current_date}.

    Résumé Global du Marché :

    CAC 40 : Clôture à {cac40_close_value:.2f}

    Si vous avez besoin des données brutes pour une analyse plus approfondie, n'hésitez pas à consulter le fichier Excel joint.

    Cordialement,
    Équipe SUP_Trading
    """

    # Chemin vers le fichier Excel généré le jour même
    excel_file = f"C:/SUP_Trading/SUP_Trading/realtime_data_{datetime.now().strftime('%Y%m%d')}.xlsx"

    # Envoi de l'email avec le fichier Excel en pièce jointe
    send_mail(subject, body, excel_file)
