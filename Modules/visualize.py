import matplotlib.pyplot as plt

def viz(data):
    """
    Affiche un graphique des données boursières.

    Args:
        data (pd.DataFrame): Les données boursières à visualiser.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(data['date'], data['adj_close'], label='Prix ajusté')
    plt.title('Historique des prix ajustés')
    plt.xlabel('Date')
    plt.ylabel('Prix ajusté')
    plt.legend()
    plt.show()
