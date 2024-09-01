import os
import traceback
import psycopg2
from psycopg2 import sql
from datetime import datetime, timedelta
import pandas as pd
import time
import yfinance as yf
from Modules.symbols import symbols
from Modules.mail_send import send_mail
from configuration.configBase import db_host, db_name, db_user, db_password

# Fonction pour se connecter à la base de données
def connect():
    try:
        connexion = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        cursor = connexion.cursor()
        print("Connexion réussie à la base de données Azure")
        return cursor, connexion
    except Exception as e:
        print(f"Erreur lors de la connexion à la base de données: {e}")
        raise

# Fonction pour créer une table
def create_table(table_name, cursor, connexion):
    try:
        cursor.execute(sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                date TIMESTAMP,
                share VARCHAR(255),
                symbol VARCHAR(255),
                open NUMERIC,
                high NUMERIC,
                low NUMERIC,
                close NUMERIC,
                adj_close NUMERIC,
                volume BIGINT
            )
        """).format(sql.Identifier(table_name)))
        connexion.commit()
        print(f"Table {table_name} créée ou déjà existante.")
    except Exception as e:
        print(f"Erreur lors de la création de la table {table_name}: {e}")
        raise

# Fonction pour insérer des données
def insert_data(table_name, cursor, connexion, data):
    try:
        query = sql.SQL("INSERT INTO {} (date, share, symbol, open, high, low, close, adj_close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)").format(sql.Identifier(table_name))
        cursor.execute(query, (
            data['date'],
            data['share'],
            data['symbol'],
            data['open'],
            data['high'],
            data['low'],
            data['close'],
            data['adj_close'],
            data['volume']
        ))
        connexion.commit()
        print(f"Données insérées dans {table_name}")
    except Exception as e:
        print(f"Erreur lors de l'insertion des données: {e}")
        raise

# Fonction pour déterminer si le script doit s'exécuter
def should_run(hour, minute):
    return (9 <= hour < 17) or (hour == 17 and minute <= 40)

# Fonction principale
def main():
    cursor = None
    connexion = None

    current_time = datetime.now()
    hour = current_time.hour
    minute = current_time.minute

    if should_run(hour, minute):
        try:
            print("Début du script")
            cursor, connexion = connect()
            create_table("cac40_daily_data", cursor, connexion)
            create_table("cac40_history_data", cursor, connexion)
            last_data = pd.DataFrame(columns=['date', 'share', 'symbol', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])

            while True:
                current_time = datetime.now()
                hour = current_time.hour
                minute = current_time.minute

                if not should_run(hour, minute):
                    print("\nHors des heures de trading. Heure actuelle: ", hour, ":", minute)
                    break  # Sortie de la boucle si hors des heures de trading

                # Récupérer les données en temps réel
                data_start_time = time.time()
                returned_data = temps_reel_data(symbols.values())  # Récupérer les données
                data_end_time = time.time()
                data_retrieval_time = data_end_time - data_start_time
                print(returned_data)

                if not returned_data.empty:
                    insertion_all_time = 0  # Initialiser le temps total d'insertion           
                    for index, row in returned_data.iterrows():
                        if not ((last_data['date'] == row['date']) & (last_data['symbol'] == row['symbol'])).any():
                            print("\nNouvelle donnée détectée.")
                            
                            # Mesurer le temps d'insertion des données
                            insert_start_time = time.time()
                            insert_data("cac40_daily_data", cursor, connexion, dict(row))  
                            insert_end_time = time.time()
                            insertion_time = insert_end_time - insert_start_time
                            insertion_all_time += insertion_time
                            
                        else:
                            print("\nDonnée existante.")
                    
                    last_data = returned_data.copy()  
                    
                    with open('execution_times.txt', 'a') as file:
                        file.write(f'Temps de récupération des données: {data_retrieval_time} secondes\n')
                        if insertion_all_time > 0:  # Écrire le temps d'insertion seulement s'il y a eu des insertions
                            file.write(f"Temps total d'insertion: {insertion_all_time} secondes\n")
                else:
                    print("\nAucune nouvelle donnée. Heure actuelle:", hour, ":", minute)

                # Vider la table si l'heure est 17h40
                if hour == 17 and minute >= 40:
                    # Récupérer toutes les données de la table
                    cursor.execute("SELECT * FROM cac40_daily_data")
                    rows = cursor.fetchall()
                    df = pd.DataFrame(rows, columns=['index','date', 'share', 'symbol', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])
                    
                    # Exporter les données dans un fichier CSV
                    csv_file_name = f'Files/cac40_daily_data_{datetime.now()}.csv'
                    df.to_csv(csv_file_name, index=False)
                    print(f"Les données ont été exportées dans le fichier {csv_file_name}.")
                    
                    # Envoi de mail
                    send_mail(f"Copie des donnees du cac40 {datetime.now()}","Bonjour\nVoici le fichier du cours des actions du CAC40 pour aujourd'hui\nCordialement Equipe IT",csv_file_name)
                    
                    cursor.execute("TRUNCATE TABLE cac40_daily_data RESTART IDENTITY")
                    connexion.commit()
                    print("Table cac40_daily_data vidée.")  
                    break
                
            cursor.close()
            connexion.close()

        except Exception as e:
            print("Oupssss, un probleme est survenu")
            error_message = f"Erreur survenue le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            error_message += "Détails de l'erreur :\n"
            error_message += str(e) + "\n\n"
            error_message += "Traceback:\n"
            error_message += traceback.format_exc()
            
            error_log_file = f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(error_log_file, "w") as file:
                file.write(error_message)
            
            send_mail("Erreur dans l'exécution du script Robot App-Sup-Trading", 
                    "Une erreur s'est produite lors de l'exécution du script. Veuillez trouver les détails de l'erreur ci-joint.\n\n", 
                    error_log_file)
            
            print("Une alerte a été envoyée!")
            print("Fin du programme avec échec\n\n")
            
            os.remove(error_log_file)
            
        finally:
            if cursor is not None:
                cursor.close()
            if connexion is not None:
                connexion.close()
                
    else:
        print("\nHors des heures de trading. Heure actuelle: ", hour, ":", minute)

if __name__ == "__main__":
    main()

