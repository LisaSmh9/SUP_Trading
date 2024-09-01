# SUP_Trading
Le robot RPA est conçu pour automatiser la collecte de données boursières du CAC40 en temps réel, leur stockage dans une base de données PostgreSQL hébergée sur Azure, et l'envoi d'un rapport quotidien par email à la fin de chaque journée de trading. Le robot s'exécute automatiquement entre 9h et 17h40 pendant les jours ouvrables.

## 2. Pré-requis
Avant d'installer et de configurer le robot, assurez-vous d'avoir les éléments suivants :

- Un serveur PostgreSQL fonctionnel sur Azure.
- Un environnement Python 3.12.4 installé.
- Accès administratif sur la machine où le robot sera exécuté.
- Configuration correcte du réseau pour permettre les connexions sortantes vers le serveur PostgreSQL sur le port 5432.
- Accès au Planificateur de tâches sous Windows.

## 3. Structure du robot
Le robot RPA développé se compose de plusieurs modules et fichiers de configuration. 

### 1. Répertoire configuration
**configBase.py :** Ce fichier contient la configuration des variables d'environnement utilisées pour se connecter à la base de données Azure. 
**configMail.json :** Ce fichier JSON contient la configuration nécessaire pour l'envoi des emails. 

### 2. Répertoire Modules
**data_save.py :** Ce module gère la sauvegarde des données collectées sous forme de fichiers CSV ou Excel. Il contient des fonctions pour enregistrer les données boursières dans des formats exploitables.
**historical_data.py :** Ce module est responsable de la collecte des données historiques sur les symboles boursiers spécifiés. Il télécharge les données depuis Yahoo Finance et les traite selon les besoins de l'utilisateur.
**mail_send.py :** Ce module gère l'envoi des emails. Il contient des fonctions envoyer les emails.
**realtime_data.py :** Ce module collecte les données en temps réel pour les symboles boursiers spécifiés. Il est utilisé pour surveiller en direct les variations des cours pendant les heures de trading.
**symbols.py :** Ce fichier contient un dictionnaire des symboles boursiers et leurs noms respectifs. Il est utilisé pour mapper les symboles aux entreprises correspondantes.
**visualize.py :** Ce module contient des fonctions pour visualiser les données boursières sous forme de graphiques. Il permet de générer des représentations visuelles des données collectées pour une meilleure compréhension.

## 4. Installation
**Cloner le Répertoire du Projet :**

Utilisez la commande suivante pour cloner le projet depuis le dépôt GitHub :

```git clone https://github.com/LisaSmh9/SUP_Trading.git``` 

**Naviguez vers le répertoire du projet :**

`cd SUP_Trading`

**Installer les Dépendances :**
Assurez-vous d'avoir pip installé, puis exécutez la commande suivante pour installer toutes les dépendances nécessaires :
`pip install -r requirements.txt`

## 5. Configuration :
### Configuration de la Base de Données
**Variables d'Environnement :**
Créez un fichier .env à la racine du projet avec les variables suivantes :

```DB_HOST=trading-server.database.windows.net
DB_NAME=trading_db
DB_USER=adminuser
DB_PASSWORD=YourPasswordHere ``` 


### Configuration de l'Environnement
Charger les Variables d'Environnement :
Les variables d'environnement définies dans le fichier .env seront automatiquement chargées par le script configBase.py.


## Configuration des Emails
### Configuration des Informations de Messagerie :
Créez un fichier configMail.json dans le répertoire configuration avec les détails suivants :

`{
    "host": "smtp.gmail.com",
    "port": 465,
    "user": "lisasmah97@gmail.com",
    "password": "*************",
    "to": "lisa.smah@supdevinci-edu.fr"
}`

## 6. Fonctionnalités du Robot
- Collecte Automatique de Données : Le robot récupère les données du CAC40 en temps réel à intervalles réguliers pendant les heures de trading.
- Stockage des Données : Les données collectées sont stockées dans une base de données PostgreSQL hébergée sur Azure.
- Envoi de Rapport : Un rapport quotidien contenant les données collectées est envoyé par email à l'équipe à la fin de chaque journée de trading.


## 7. Planification des Tâches
Création d'une Tâche Planifiée sous Windows
Ouvrir le Planificateur de Tâches :

Ouvrez Gestion de l'ordinateur > Planificateur de tâches.
Créer une Nouvelle Tâche :
Cliquez sur Créer une tâche....
Donnez un nom à la tâche (par exemple, "Collecte de données boursières").

Configurer l'Exécution :
Dans l'onglet Déclencheurs, ajoutez un nouveau déclencheur pour exécuter la tâche tous les jours ouvrables à 9h00.

Configurer l'Action :
Dans l'onglet Actions, configurez l'action pour exécuter le script Python robot_azure.py.
Chemin du script :
`C:\...\Programs\Python\Python312\python.exe`
Argument :
`C:\chemin\vers\SUP_Trading\Modules\robot_azure.py`
Configurer les Conditions et Paramètres :

Définissez les conditions pour que la tâche s'exécute uniquement si la machine est allumée et non en mode batterie, par exemple.
Finaliser et Tester :

Enregistrez la tâche et testez-la pour vous assurer qu'elle fonctionne correctement.

## 8. Exécution Manuelle
Pour exécuter le robot manuellement, ouvrez un terminal dans le répertoire du projet et exécutez :
`python -m Modules.robot_azure`

## 9. FAQ
Q: Comment puis-je changer l'heure de collecte des données ?

A: Modifiez le déclencheur dans le Planificateur de tâches pour exécuter le script à l'heure souhaitée.

Q: Comment puis-je ajouter de nouveaux symboles à surveiller ?

A: Ajoutez les nouveaux symboles dans le fichier symbols.py.

## Conclusion
Ce robot RPA est conçu pour automatiser efficacement le processus de collecte, de stockage et de rapport des données boursières. Sa structure modulaire permet une grande flexibilité et une maintenance aisée. En suivant ce manuel, vous devriez être en mesure de configurer et d'exécuter le robot sans difficulté
