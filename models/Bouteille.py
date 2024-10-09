from models.Connexion import create_connection
#from models.etagere import Etagere peut etre faire lien entre les pages
#from models.vin import Vin

class Bouteille:
    def __init__(self, shelf_id, winery, name, type, year, region, comments, personal_rating, community_rating, label_photo, price):
        self.shelf_id = shelf_id
        self.winery = winery
        self.name = name
        self.type = type
        self.year = year
        self.region = region
        self.comments = comments
        self.personal_rating = personal_rating
        self.community_rating = community_rating
        self.label_photo = label_photo
        self.price = price

    def ajouter_bouteille(self):
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO bottles (shelf_id, winery, name, type, year, region, comments, personal_rating, community_rating, label_photo, price)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (self.shelf_id, self.winery, self.name, self.type, self.year, self.region, self.comments, self.personal_rating, self.community_rating, self.label_photo, self.price))
        
        connection.commit()
        connection.close()
        print("Bouteille ajoutée avec succès.")

    def supprimer_bouteille(self, bottle_id):
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM bottles WHERE bottle_id=%s", (bottle_id,))
        connection.commit()
        connection.close()
        print("Bouteille supprimée avec succès.")
