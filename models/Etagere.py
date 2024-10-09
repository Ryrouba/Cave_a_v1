from models.Connexion import create_connection

class Etagere:
    def __init__(self, cave_id, shelf_name, shelf_number, region, available_slots, bottles_per_shelf):
        self.cave_id = cave_id
        self.shelf_name = shelf_name  # Ajout de l'attribut shelf_name
        self.shelf_number = shelf_number
        self.region = region
        self.available_slots = available_slots
        self.bottles_per_shelf = bottles_per_shelf

    def ajouter_etagere(self):
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO shelves (cave_id, shelf_name, shelf_number, region, available_slots, bottles_per_shelf)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (self.cave_id, self.shelf_name, self.shelf_number, self.region, self.available_slots, self.bottles_per_shelf))
        
        connection.commit()
        connection.close()
        print("Étagère ajoutée avec succès.")

    def supprimer_etagere(self, shelf_id):
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM shelves WHERE shelf_id=%s", (shelf_id,))
        connection.commit()
        connection.close()
        print("Étagère supprimée avec succès.")
