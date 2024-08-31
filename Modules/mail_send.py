import json
import smtplib
from email.message import EmailMessage
import mimetypes
import logging

# Configuration du logging (meilleure gestion des erreurs et des journaux)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_email_config(config_path: str):
    """
    Charge la configuration de l'email à partir d'un fichier JSON.

    :param config_path: Chemin vers le fichier de configuration.
    :return: Dictionnaire contenant la configuration de l'email.
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

    :param subject: Sujet de l'email.
    :param body: Corps du message de l'email.
    :param sender: Adresse email de l'expéditeur.
    :param recipients: Liste des adresses email des destinataires.
    :param attachment: Chemin vers le fichier à attacher à l'email.
    :return: Objet EmailMessage.
    """
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg.set_content(body)

        # Attache le fichier spécifié à l'email.
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

    :param msg: L'objet EmailMessage à envoyer.
    :param email_config: Dictionnaire contenant la configuration de l'email (hôte, port, utilisateur, mot de passe).
    """
    try:
        with smtplib.SMTP_SSL(email_config['host'], email_config['port']) as server:
            server.login(email_config['user'], email_config['password'])
            server.send_message(msg)
        logging.info("Email envoyé avec succès.")
    except Exception as e:
        logging.error(f"Echec de l'envoi de l'email : {e}")
        raise

def send_mail(subject: str, body: str, attachment: str):
    """
    Envoie un email avec un sujet, un corps de message et une pièce jointe.

    :param subject: Sujet de l'email.
    :param body: Corps du message de l'email.
    :param attachment: Chemin vers le fichier à attacher à l'email.
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
    send_mail("Test Subject", "This is a test email body", "C:/Users/lisas/Downloads/SupTrading/SupTrading/attachment.txt")
