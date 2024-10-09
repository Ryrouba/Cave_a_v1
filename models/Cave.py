from models.Connexion import create_connection

class Cave:
    def __init__(self, user_id, cave_name):
        self.user_id = user_id
        self.cave_name = cave_name

    def ajouter_cave(self):
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO caves (user_id, cave_name)
            VALUES (%s, %s)
        """, (self.user_id, self.cave_name))
        
        connection.commit()
        connection.close()
        print("Cave ajoutée avec succès.")

    def supprimer_cave(self, cave_id):
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM caves WHERE cave_id=%s", (cave_id,))
        connection.commit()
        connection.close()
        print("Cave supprimée avec succès.")
