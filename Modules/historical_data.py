import logging
import pandas as pd
from datetime import datetime
import yfinance as yf
from Modules.symbols import symbols as sb
from Modules.data_save import save_to
from Modules.visualize import viz  # Importation de la fonction viz

# Configuration du logging
logging.basicConfig(level=logging.INFO, filename="./Log/SupTrading.log", filemode="a", format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_key(value):
    return next((key for key, val in sb.items() if val == value), None)

def process_hist(symbol, data):
    while True:
        print("\nVeuillez choisir une option:\n")
        print("1- Stocker l'historique dans un fichier\n2- Visualiser l'historique (Graphe)\n3- Retour\n")
        option = input()
        
        if option == "1":
            format = input("\nVeuillez choisir le format du fichier (csv/xlsx):\n")
            if save_to(get_key(symbol), data, format):
                logger.info(f"Historique du symbole {symbol} sauvegardé avec succès.")
            break
        elif option == "2":
            viz(data)  # Appel de la fonction viz importée de visualize.py
            logger.info(f"Historique du symbole {symbol} visualisé avec succès.")
        elif option == "3":
            return
        else:
            print("Oupssss, option non disponible")

def download_hist_data(symbol, start, end, interval, period, option):
    try:
        if option == 1:
            data = yf.download(symbol, start=start, end=end, interval=interval)
        elif option == 2:
            data = yf.download(symbol, period=period)
        
        data.reset_index(inplace=True)
        share = get_key(symbol)
        data['share'] = share
        data['symbol'] = symbol
        data.rename(columns={'Adj Close': 'adj_close'}, inplace=True)
        data.columns = data.columns.str.lower()
        
        logger.info(f"Traitement de l'historique pour le symbole {symbol}.")
        process_hist(symbol, data)
        logger.info(f"Fin du traitement pour {symbol}.")
    except Exception as e:
        logger.error(f"Erreur lors du traitement de l'historique pour {symbol}: {e}")

if __name__ == "__main__":
    download_hist_data("AC.PA", "2024-01-01", "2024-08-31", "1d", None, 1)
