from Connexion import create_connection

def create_tables():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        # Création des tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS caves (
                cave_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                cave_name VARCHAR(255) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shelves (
                shelf_id INT AUTO_INCREMENT PRIMARY KEY,
                cave_id INT,
                shelf_name VARCHAR(255) NOT NULL,
                
                FOREIGN KEY (cave_id) REFERENCES caves(cave_id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bottles (
                bottle_id INT AUTO_INCREMENT PRIMARY KEY,
                shelf_id INT,
                winery VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                type VARCHAR(100) NOT NULL,
                year INT NOT NULL,
                region VARCHAR(100) NOT NULL,
                comments TEXT,
                personal_rating FLOAT,
                community_rating FLOAT,
                label_photo VARCHAR(255),
                price DECIMAL(10, 2),
                FOREIGN KEY (shelf_id) REFERENCES shelves(shelf_id) ON DELETE CASCADE
            )
        """)

        connection.commit()
        print("Tables créées avec succès.")

    except Exception as e:
        print(f"Erreur : {e}")
    finally:
        cursor.close()
        connection.close()
        print("Connexion à la base de données fermée.")

