const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
app.use((req, res, next) => {
    res.header("Access-Control-Allow-Origin", "*"); // Autorise tout le monde
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    res.header("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
    next();
});
app.use(bodyParser.json());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.json());

const db = mysql.createPool({ // On utilise "createPool" au lieu de "createConnection"
    host: "127.0.0.1",
    user: "root",
    password: "", 
    database: "ecoprix_db",
    waitForConnections: true,
    connectionLimit: 10
});

// On vérifie la connexion une fois
db.getConnection((err, connection) => {
    if (err) console.log("Erreur de connexion :", err);
    else {
        console.log("Connecté à MySQL avec succès !");
        connection.release();
    }
});

// Route pour afficher la page
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

// Route pour LIRE les prix
app.get('/api/prix', (req, res) => {
    db.query("SELECT * FROM produits ORDER BY id DESC", (err, result) => {
        if (err){
            console.log(err);
             res.status(500).send(err);
        }
        else{ res.json(result);

        }
    });
});

// Route pour AJOUTER un prix
app.post('/api/prix', (req, res) => {
    const { nom, prix, marche, categorie, unite, saison } = req.body;
    const sql = "INSERT INTO produits (nom_produit, prix, marche, categorie, unite, saison) VALUES (?, ?, ?, ?, ?, ?)";
    db.query(sql, [nom, prix, marche, categorie, unite, saison], (err, result) => {
        if (err) res.status(500).send(err);
        else res.status(201).send("Donnée ajoutée !");
    });
});

app.listen(3000, () => console.log("Serveur prêt sur http://localhost:3000"));