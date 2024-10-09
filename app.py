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

        user_info = {
            'username': username,
            'num_shelves': num_shelves,
            'bottles_count': bottles_count,
            'num_caves': num_caves
            }
        
        cursor.close()
        connection.close()

        return render_template('accueil.html', user_info=user_info)  # Remplacez par votre fichier HTML d'accueil
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

#-----------------------------------------------------------------------------------------------------------------------
# Route Déconnexion
#-----------------------------------------------------------------------------------------------------------------------
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect('/')
#-----------------------------------------------------------------------------------------------------------------------

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

#-----------------------------------------------------------------------------------------------------------------------
# Route Bouteille.html
#-----------------------------------------------------------------------------------------------------------------------
@app.route("/bouteille", methods=["GET", "POST"])
def bouteille():
    if 'username' in session:
        user_id = session.get('user_id')

        if request.method == "POST":
            winery = request.form.get("winery")
            name = request.form.get("name")
            type = request.form.get("type")
            year = request.form.get("year")
            region = request.form.get("region")
            comments = request.form.get("comments")
            personal_rating = request.form.get("personal_rating")
            community_rating = request.form.get("community_rating")
            price = request.form.get("price")
            shelf_id = request.form.get("shelf_id")

            connection = create_connection()  # Utilisation de votre méthode de connexion
            cursor = connection.cursor()

            insert_query = "INSERT INTO bottles (winery, name, type, year, region, comments, personal_rating, community_rating, price, shelf_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            bottle_data = (winery, name, type, year, region, comments, personal_rating, community_rating, price, shelf_id)
            cursor.execute(insert_query, bottle_data)

            connection.commit()
            cursor.close()
            connection.close()

            return redirect("/accueil")
        else:
            connection = create_connection()
            cursor = connection.cursor()

            # Récupérer les étagères de l'utilisateur
            get_shelves_query = "SELECT shelf_id, shelf_number FROM shelves WHERE cave_id IN (SELECT cave_id FROM caves WHERE user_id = %s)"
            cursor.execute(get_shelves_query, (user_id,))
            shelves = cursor.fetchall()

            # Récupérer les bouteilles de l'utilisateur
            get_bottles_query = "SELECT * FROM bottles WHERE shelf_id IN (SELECT shelf_id FROM shelves WHERE cave_id IN (SELECT cave_id FROM caves WHERE user_id = %s))"
            cursor.execute(get_bottles_query, (user_id,))
            bottles = cursor.fetchall()

            cursor.close()
            connection.close()

            return render_template('bouteille.html', shelves=shelves, bottles=bottles)
    else:
        return redirect("/accueil")
#-----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
    