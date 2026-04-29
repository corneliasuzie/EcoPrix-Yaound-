import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app) # C'est l'équivalent de ton "app.use(cors())"

# Configuration de la base de données (Railway ou Local)
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get('MYSQLHOST', '127.0.0.1'),
        user=os.environ.get('MYSQLUSER', 'root'),
        password=os.environ.get('MYSQLPASSWORD', ''),
        database=os.environ.get('MYSQLDATABASE', 'ecoprix_db'),
        port=int(os.environ.get('MYSQLPORT', 3306))
    )

# 1. Route pour afficher la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# 2. Route pour LIRE les prix (GET /api/prix)
@app.route('/api/prix', methods=['GET'])
def get_prix():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM produits ORDER BY id DESC")
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 3. Route pour AJOUTER un prix (POST /api/prix)
@app.route('/api/prix', methods=['POST'])
def add_prix():
    try:
        data = request.json
        nom = data.get('nom')
        prix = data.get('prix')
        marche = data.get('marche')
        categorie = data.get('categorie')
        unite = data.get('unite')
        saison = data.get('saison')

        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO produits (nom_produit, prix, marche, categorie, unite, saison) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (nom, prix, marche, categorie, unite, saison)
        
        cursor.execute(sql, values)
        conn.commit() # Très important en Python pour enregistrer
        cursor.close()
        conn.close()
        
        return "Donnée ajoutée !", 201
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    # Railway utilise la variable d'environnement PORT
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)