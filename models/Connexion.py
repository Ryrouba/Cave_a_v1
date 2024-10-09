# connexion.py
import mysql.connector
from mysql.connector import Error

def create_connection():
    """Créer une connexion à la base de données MySQL."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host='0.0.0.0',  # Adresse IP de votre serveur MySQL
            port=3306,        # Port du serveur MySQL
            user='root',      # Nom d'utilisateur MySQL
            password='Ryanbaba73',  # Mot de passe MySQL
            database='cave_a_v1'  # Nom de la base de données
        )
        print("Connexion à la base de données réussie.")
    except Error as e:
        print(f"Erreur lors de la connexion à la base de données: {e}")
    
    return connection
