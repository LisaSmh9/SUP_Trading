import logging
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
from Modules.symbols import symbols as sb

# Configuration du logging
logging.basicConfig(level=logging.INFO, filename="./Log/SupTrading.log", filemode="a", format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_key(value):
    """
    Cherche dans le dictionnaire des symbols la cle qui correspond a la valeur passee en parametre

    Args:
        value (string): le symbol d'une action du cac40

    Returns:
        key_wanted (string): la cle qui correspond a la value
    """
    return next((key for key, val in sb.items() if val == value), None)

def download_realtime_data(symbols):
    """
    Télécharge et traite les données en temps réel pour une liste de symboles boursiers.

    Args:
        symbols (list): Liste des symboles boursiers à traiter.

    Returns:
        pd.DataFrame: DataFrame contenant les dernières données pour tous les symboles fournis.
    """
    final_rows = []
    for symbol in symbols:
        share = get_key(symbol)
        if not share:
            logger.error(f"Symbole non trouvé: {symbol}")
            continue
        
        try:
            now = datetime.now()
            start = now - timedelta(minutes=120)
            data = yf.download(symbol, start=start, interval="1m")
            data.reset_index(inplace=True)
            data['share'] = share
            data['symbol'] = symbol
            data.rename(columns={'Datetime': 'date', 'Adj Close': 'adj_close'}, inplace=True)
            data.columns = data.columns.str.lower()
            final_row = data.tail(1)
            final_rows.append(final_row)
        except Exception as e:
            logger.error(f"Erreur lors du téléchargement des données pour {symbol}: {e}")
    
    if final_rows:
        return pd.concat(final_rows)
    else:
        return pd.DataFrame()

if __name__ == "__main__":
    # Vérifie si le jour actuel est un jour de semaine (lundi=0, dimanche=6)
    if datetime.now().weekday() >= 5:
        print("Le marché est fermé, aucune donnée en temps réel n'est disponible.")
    else:
        symbols_list = ["AC.PA", "AI.PA"]  # "Accor": "AC.PA", "Air Liquide": "AI.PA"
        real_time_data = download_realtime_data(symbols_list)
        print(real_time_data)