from models.Connexion import create_connection

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def ajouter_utilisateur(self):
        try:
            connection = create_connection()
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO users (username, password)
                VALUES (%s, %s)
            """, (self.username, self.password))
            connection.commit()
            print("Utilisateur ajouté avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'utilisateur : {e}")
            raise  # Re-levez l'exception pour la gestion dans l'appelant
        finally:
            connection.close()
