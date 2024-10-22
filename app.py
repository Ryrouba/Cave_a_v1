#-----------------------------------------------------------------------------------------------------------------------
#                   IMPORTATION DES MODULES PYTHON
#-----------------------------------------------------------------------------------------------------------------------
from models.Users import User
from models.Cave import Cave
from models.Bouteille import Bouteille
from models.Etagere import Etagere
from models.Connexion import create_connection
from flask import Flask, render_template, request, redirect, session, flash, url_for
from notifypy import Notify
import os
import json
from flask import jsonify, send_file
from decimal import Decimal
#-----------------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
app.secret_key = os.urandom(24)


#-----------------------------------------------------------------------------------------------------------------------
#                   DESCRIPTION DES ROUTES
#-----------------------------------------------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('signup.html')

#-----------------------------------------------------------------------------------------------------------------------
# Route Accueil.html
#-----------------------------------------------------------------------------------------------------------------------
@app.route('/accueil')
def accueil():
    if 'username' in session:
        username = session['username']

        connection = create_connection()
        cursor = connection.cursor()

        query = "SELECT COUNT(*) FROM shelves INNER JOIN caves ON shelves.cave_id = caves.cave_id WHERE caves.user_id = %s"
        cursor.execute(query, (session['user_id'],))
        num_shelves = cursor.fetchone()[0]

        query = "SELECT COUNT(*) FROM bottles INNER JOIN shelves ON bottles.shelf_id = shelves.shelf_id INNER JOIN caves ON shelves.cave_id = caves.cave_id WHERE caves.user_id = %s"
        cursor.execute(query, (session['user_id'],))
        bottles_count = cursor.fetchone()[0]

        query = "SELECT COUNT(*) FROM caves WHERE user_id = %s"  # Nouvelle requête pour compter le nombre de caves
        cursor.execute(query, (session['user_id'],))
        num_caves = cursor.fetchone()[0]

        # Récupérer tous les commentaires des bouteilles
        cursor.execute("SELECT name, comments FROM bottles")
        commentaires = cursor.fetchall()  # Récupère tous les commentaires sous forme de liste de tuples

        user_info = {
            'username': username,
            'num_shelves': num_shelves,
            'bottles_count': bottles_count,
            'num_caves': num_caves
            }
        
        cursor.close()
        connection.close()

        return render_template('accueil.html', user_info=user_info, commentaires=commentaires)  # Remplacez par votre fichier HTML d'accueil
    else:
        return render_template('accueil.html')

#-----------------------------------------------------------------------------------------------------------------------
# Route pour Connexion
#-----------------------------------------------------------------------------------------------------------------------
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username").strip()  # Enlever les espaces
        password = request.form.get("password").strip()  # Enlever les espaces

        connection = create_connection()  # Utilisation de votre méthode de connexion
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        print("User fetched from database:", user)  # Affiche les détails de l'utilisateur récupéré

        # Vérification des identifiants
        if user and user[2] == password:
            session['username'] = username
            session['user_id'] = user[0]  # Sauvegarde de l'ID de l'utilisateur dans la session
            return redirect("/accueil")
        else:
            notification = Notify()
            notification.title = "IDENTIFIANTS INCORRECTS"
            notification.message = 'Veuillez réessayer !'
            notification.icon = "static/images/notif.png"
            notification.timeout = 5000
            notification.send()

            return redirect("/signup")
        
#-----------------------------------------------------------------------------------------------------------------------
# Route Déconnexion
#-----------------------------------------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/')

#-----------------------------------------------------------------------------------------------------------------------
# Route pour inscription
#-----------------------------------------------------------------------------------------------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        
        try:
            user.ajouter_utilisateur()
            flash('User registered successfully!', 'success')
            return redirect(url_for('index'))  # Rediriger vers l'index après l'inscription
        except Exception as e:
            flash(f'Error creating user: {str(e)}', 'danger')
            return redirect(url_for('create_user'))  # Redirige vers la page d'inscription en cas d'erreur
    else:
        return render_template('signup.html')

#-----------------------------------------------------------------------------------------------------------------------
# Route Bouteille.html
#-----------------------------------------------------------------------------------------------------------------------
@app.route("/bouteille", methods=["GET", "POST"])
def bouteille():
    if 'username' in session:
        user_id = session.get('user_id')

        if request.method == "POST":
            # Traitez l'ajout de bouteille ici
            winery = request.form.get('winery')
            name = request.form.get('name')
            type = request.form.get('type')
            year = request.form.get('year')
            region = request.form.get('region')
            comments = request.form.get('comments')
            personal_rating = request.form.get('personal_rating')
            community_rating = request.form.get('community_rating')
            label_photo = request.form.get('label_photo')
            price = request.form.get('price')
            shelf_id = request.form.get('shelf_id')

            # Connexion à la base de données pour insérer la nouvelle bouteille
            connection = create_connection()
            cursor = connection.cursor()

            # Vérification du nombre de places disponibles
            cursor.execute("SELECT available_slots FROM shelves WHERE shelf_id = %s", (shelf_id,))
            available_slots = cursor.fetchone()

            if available_slots and available_slots[0] > 0:

            # Requête d'insertion pour la nouvelle bouteille
                insert_bottle_query = """
                    INSERT INTO bottles (winery, name, type, year, region, comments, personal_rating, community_rating, label_photo, price, shelf_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_bottle_query, (winery, name, type, year, region, comments, personal_rating, community_rating, label_photo, price, shelf_id))

                # Mise à jour du nombre de places disponibles
                cursor.execute("UPDATE shelves SET available_slots = available_slots - 1 WHERE shelf_id = %s", (shelf_id,))

                connection.commit()  # Ne pas oublier de valider la transaction
                flash("Bouteille ajoutée avec succès.")  # Message de succès
            else:
                flash("Pas assez de place disponible sur l'étagère.")  # Message d'erreur

            cursor.close()
            connection.close()

            return redirect("/bouteille")  # Redirige vers la page des bouteilles après ajout

        else:
            # Récupérer l'étagère sélectionnée via le bouton
            selected_shelf_id = request.args.get('shelf_id', None)

            # Convertir selected_shelf_id en entier si disponible
            if selected_shelf_id is not None:
                selected_shelf_id = int(selected_shelf_id)

            # Connexion à la base de données pour récupérer les étagères
            connection = create_connection()
            cursor = connection.cursor()

            # Requête pour récupérer les bouteilles de l'étagère sélectionnée
            if selected_shelf_id is not None:
                get_bottles_query = """
                    SELECT * FROM bottles WHERE shelf_id = %s
                """
                cursor.execute(get_bottles_query, (selected_shelf_id,))
            else:
                # Si aucune étagère n'est sélectionnée, on récupère toutes les bouteilles
                get_bottles_query = """
                    SELECT * FROM bottles
                    WHERE shelf_id IN (SELECT shelf_id FROM shelves WHERE cave_id IN (SELECT cave_id FROM caves WHERE user_id = %s))
                """
                cursor.execute(get_bottles_query, (user_id,))

            bottles = cursor.fetchall()

            # Récupération des étagères disponibles
            get_shelves_query = """
                SELECT shelves.shelf_id, shelves.shelf_number, shelves.shelf_name, caves.cave_name
                FROM shelves
                JOIN caves ON shelves.cave_id = caves.cave_id
                WHERE caves.user_id = %s;
            """
            cursor.execute(get_shelves_query, (user_id,))
            shelves = cursor.fetchall()

            cursor.close()
            connection.close()

            return render_template('bouteille.html', shelves=shelves, bottles=bottles, selected_shelf_id=selected_shelf_id)
    else:
        return redirect("/accueil")

#-----------------------------------------------------------------------------------------------------------------------
# Route /Supprimer_bouteille
#-----------------------------------------------------------------------------------------------------------------------
@app.route("/supprimer_bouteille/<int:bottle_id>", methods=["POST"])
def supprimer_bouteille(bottle_id):
    if 'user_id' not in session:
        return redirect("/accueil")  # Redirection si l'utilisateur n'est pas connecté

    # Créer une instance de Bouteille pour appeler la méthode de suppression
    bouteille = Bouteille(None, None, None, None, None, None, None, None, None, None, None)
    bouteille.supprimer_bouteille(bottle_id)  # Appel de la méthode pour supprimer la bouteille

    return redirect(url_for('bouteille'))  # Rediriger vers la page d'affichage des bouteilles

#-----------------------------------------------------------------------------------------------------------------------
# Route /Créer_cave
#-----------------------------------------------------------------------------------------------------------------------
@app.route("/cave", methods=["GET", "POST"], endpoint="cave")
def afficher_et_gestion_caves():
    if 'user_id' not in session:
        return redirect("/accueil")  # Rediriger vers la page de connexion si l'utilisateur n'est pas connecté

    user_id = session['user_id']

    # Si c'est une requête POST, cela signifie que l'utilisateur souhaite créer une nouvelle cave
    if request.method == "POST":
        cave_name = request.form.get("cave_name")

        if cave_name:
            # Utiliser la classe Cave pour ajouter une cave
            nouvelle_cave = Cave(user_id, cave_name)
            nouvelle_cave.ajouter_cave()

        return redirect("/cave")  # Recharger la page pour actualiser la liste des caves

    # Requête GET : Afficher la page avec la liste des caves
    connection = create_connection()
    cursor = connection.cursor()

    # Obtenir la liste des caves de l'utilisateur
    cursor.execute("SELECT cave_id, cave_name FROM caves WHERE user_id = %s", (user_id,))
    caves = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("cave.html", caves=caves)


@app.route("/supprimer_cave/<int:cave_id>", methods=["POST"])
def supprimer_cave(cave_id):
    # Vérifier si l'utilisateur est connecté
    if 'user_id' not in session:
        return redirect("/accueil")  # Rediriger vers la page d'accueil si non connecté
    
    user_id = session['user_id']

    # Connexion à la base de données pour vérifier si la cave appartient à l'utilisateur
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT cave_id FROM caves WHERE cave_id = %s AND user_id = %s", (cave_id, user_id))
    cave = cursor.fetchone()

    connection.close()

    if cave:
        # La cave appartient à l'utilisateur, on utilise la méthode de la classe Cave pour la supprimer
        cave_instance = Cave(user_id, "")  # L'utilisateur est nécessaire mais pas le nom de la cave ici
        cave_instance.supprimer_cave(cave_id)
        print(f"Cave {cave_id} supprimée avec succès.")
    else:
        print(f"Tentative de suppression d'une cave non existante ou non autorisée: {cave_id}")
    
    return redirect("/cave")  # Rediriger vers la page des caves après la suppression

#-----------------------------------------------------------------------------------------------------------------------
# Route /Créer_étagère
#-----------------------------------------------------------------------------------------------------------------------
@app.route("/creer_etagere", methods=["GET", "POST"], endpoint="etagere")
def creer_etagere():
    if 'user_id' not in session:
        return redirect("/accueil")  # Rediriger vers la page d'accueil si l'utilisateur n'est pas connecté

    user_id = session.get('user_id')  # Récupérer l'ID de l'utilisateur connecté depuis la session

    if request.method == "POST":
        shelf_name = request.form.get("shelf_name")
        shelf_number = request.form.get("shelf_number")
        region = request.form.get("region")
        available_slots = request.form.get("available_slots")
        bottles_per_shelf = request.form.get("bottles_per_shelf")
        cave_id = request.form.get("cave_id")  # Récupérer l'ID de la cave sélectionnée

        if not user_id or not cave_id:
            return "Erreur: ID utilisateur ou cave invalide."

        # Créer une nouvelle instance d'Etagere
        new_shelf = Etagere(cave_id=cave_id,  # Utiliser cave_id directement ici
                            shelf_name=shelf_name,
                            shelf_number=shelf_number,
                            region=region,
                            available_slots=available_slots,
                            bottles_per_shelf=bottles_per_shelf)

        # Appeler la méthode pour ajouter l'étagère
        new_shelf.ajouter_etagere()

        return redirect("/accueil")
    else:
        connection = create_connection()
        cursor = connection.cursor()
        
        # Obtenir les caves de l'utilisateur
        get_caves_query = "SELECT cave_id, cave_name FROM caves WHERE user_id = %s"
        cursor.execute(get_caves_query, (user_id,))
        caves = cursor.fetchall()

        # Récupérer toutes les étagères de l'utilisateur pour les afficher
        cursor.execute("""
            SELECT shelves.shelf_id, shelves.shelf_name, shelves.shelf_number, caves.cave_name
            FROM shelves
            INNER JOIN caves ON shelves.cave_id = caves.cave_id
            WHERE caves.user_id = %s
        """, (user_id,))
        etageres = cursor.fetchall()
        
        cursor.close()
        connection.close()

        return render_template("etagere.html", caves=caves, etageres=etageres)

#-----------------------------------------------------------------------------------------------------------------------
# Route /supprimer_étagère
#-----------------------------------------------------------------------------------------------------------------------
@app.route("/supprimer_etagere/<int:shelf_id>", methods=["POST"])
def supprimer_etagere(shelf_id):
    # Vérifier si l'utilisateur est connecté
    if 'user_id' not in session:
        return redirect("/accueil")  # Rediriger vers la page d'accueil si non connecté

    user_id = session['user_id']

    # Connexion à la base de données pour vérifier si l'étagère appartient à une cave de l'utilisateur
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT shelves.shelf_id 
        FROM shelves
        INNER JOIN caves ON shelves.cave_id = caves.cave_id
        WHERE shelves.shelf_id = %s AND caves.user_id = %s
    """, (shelf_id, user_id))
    
    etagere = cursor.fetchone()

    connection.close()

    if etagere:
        # L'étagère appartient à l'utilisateur, on peut la supprimer
        etagere_instance = Etagere(None, None, None, None, None, None)  # On initialise l'objet sans valeurs utiles
        etagere_instance.supprimer_etagere(shelf_id)
        print(f"Étagère {shelf_id} supprimée avec succès.")
    else:
        print(f"Tentative de suppression d'une étagère non existante ou non autorisée: {shelf_id}")

    return redirect("/creer_etagere")  # Rediriger vers la page des étagères après suppression

#-----------------------------------------------------------------------------------------------------------------------
# Export cave en JSON
#-----------------------------------------------------------------------------------------------------------------------
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convertir Decimal en float
        return super(DecimalEncoder, self).default(obj)

@app.route("/export_json", methods=["GET"])
def export_json():
    if 'user_id' not in session:
        return redirect("/accueil")  # Rediriger si l'utilisateur n'est pas connecté
    
    user_id = session['user_id']  # Obtenir l'utilisateur connecté

    connection = create_connection()
    cursor = connection.cursor()

    # Dictionnaire pour stocker les tables à exporter
    database_export = {}

    # 1. Exporter la table 'users' pour l'utilisateur connecté
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    users_data = cursor.fetchall()
    column_names_users = [i[0] for i in cursor.description]
    database_export['users'] = [dict(zip(column_names_users, user)) for user in users_data]

    # 2. Exporter la table 'shelves' pour les étagères appartenant à l'utilisateur connecté
    cursor.execute("""
        SELECT shelves.* 
        FROM shelves 
        INNER JOIN caves ON shelves.cave_id = caves.cave_id 
        WHERE caves.user_id = %s
    """, (user_id,))
    shelves_data = cursor.fetchall()
    column_names_shelves = [i[0] for i in cursor.description]
    database_export['shelves'] = [dict(zip(column_names_shelves, shelf)) for shelf in shelves_data]

    # 3. Exporter la table 'bottles' pour les bouteilles dans les étagères de l'utilisateur connecté
    cursor.execute("""
        SELECT bottles.* 
        FROM bottles 
        INNER JOIN shelves ON bottles.shelf_id = shelves.shelf_id
        INNER JOIN caves ON shelves.cave_id = caves.cave_id
        WHERE caves.user_id = %s
    """, (user_id,))
    bottles_data = cursor.fetchall()
    column_names_bottles = [i[0] for i in cursor.description]
    database_export['bottles'] = [dict(zip(column_names_bottles, bottle)) for bottle in bottles_data]

    # Sauvegarder les données dans un fichier JSON avec l'encodeur personnalisé
    with open("exported_database.json", "w") as json_file:
        json.dump(database_export, json_file, indent=4, cls=DecimalEncoder)

    cursor.close()
    connection.close()

    # Envoyer le fichier JSON à l'utilisateur
    return send_file("exported_database.json", as_attachment=True)


#-----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run(debug=True)
    