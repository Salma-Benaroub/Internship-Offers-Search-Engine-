from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask import session
import logging
from os import urandom


app = Flask(__name__)
CORS(app)
app.secret_key= urandom(24)

# Configuration de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = "d@taengineer2001"
app.config['MYSQL_DB'] = 'proj_tutore'


mysql = MySQL(app)


@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Adresse email ou mot de passe manquant'}), 400  # Code d'erreur 400 pour une mauvaise demande

    cur = mysql.connection.cursor()
    cur.execute("SELECT idetudiant, email, password FROM etudiant WHERE email = %s AND password = %s", (email, password))
    user = cur.fetchone()
    cur.close()

    if user:
       # L'utilisateur est trouvé dans la base de données, connexion réussie
        user_id = user[0] 
        session['idetudiant'] = user_id  # Stocke l'ID de l'utilisateur dans la session
        logging.info('Connexion réussie pour l\'utilisateur avec ID : %s', user_id)
        return jsonify({'message': 'Connexion réussie', 'user_id': user_id})
    else:
        # L'utilisateur n'est pas trouvé dans la base de données, connexion échouée
        return jsonify({'error': 'Adresse email ou mot de passe incorrect'}), 401  # Code d'erreur 401 pour une authentification échouée


@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    email = request.form.get('email')
    # Logique pour envoyer un email de réinitialisation du mot de passe
    return jsonify({'message': 'Password reset email sent!'}), 200

if __name__ == '__main__':
    app.run(port=5005,debug=True)
