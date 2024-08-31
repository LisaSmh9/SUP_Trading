from datetime import datetime
import logging
import os

import pandas as pd  # Assurez-vous que pandas est importé pour utiliser les fonctions to_csv et to_excel

# Configuration du logger
logging.basicConfig(level=logging.INFO, filename="./Log/SupTrading.log", filemode="a", format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def save_to(action, data, ext):
    """
    Sauvegarde les données dans un fichier CSV ou Excel en fonction de l'extension spécifiée.

    :param action: Nom de l'action ou identifiant pour nommer le fichier.
    :param data: DataFrame contenant les données à sauvegarder.
    :param ext: Extension du fichier pour déterminer le format de sauvegarde ('csv' ou 'xlsx').
    :return: Booléen indiquant si la sauvegarde a réussi ou non.
    """
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    directory = "./Files"
    
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Dossier {directory} créé.")

    filename = f"{directory}/{action}_historique_{current_time}.{ext}"
    
    try:
        if ext == "csv":
            data.to_csv(filename, index=False)
        elif ext == "xlsx":
            data.to_excel(filename, index=False)
        else:
            logger.warning(f"Extension '{ext}' incorrecte. Aucun fichier n'a été sauvegardé.")
            print("\nOupssss, extension incorrecte\n")
            return False
        
        logger.info(f"Fichier {filename} sauvegardé avec succès.")
        print("\nFichier sauvegardé\n")
        return True

    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde du fichier {filename}: {e}", exc_info=True)
        print(f"\nOupssss, un problème est survenu: {e}\n")
        return False

# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple de données de test
    data = pd.DataFrame({
        'Date': [datetime.now().strftime('%Y-%m-%d')],
        'Prix': [100],
        'Variation': [1.5]
    })

    # Sauvegarder en CSV
    if save_to("TestAction", data, "csv"):
        print("Sauvegarde CSV réussie.")
    else:
        print("Échec de la sauvegarde CSV.")

    # Sauvegarder en Excel
    if save_to("TestAction", data, "xlsx"):
        print("Sauvegarde Excel réussie.")
    else:
        print("Échec de la sauvegarde Excel.")
