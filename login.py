from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import ListaSpesa, db

app = Flask(__name__)

# Configurazione database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lista.db'  # URL del database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disabilita il tracciamento delle modifiche

db.init_app(app)  # Inizializzazione del database

with app.app_context():  # Creazione del contesto applicativo
    db.create_all()  # Crea le tabelle del database basate sui modelli

# Rotta principale
@app.route('/')
def home():
    return render_template('index.html')  # Renderizza la pagina principale con i pulsanti Accedi e Registrati

# Rotta per accedere
@app.route('/accedi', methods=['POST'])
def accedi():
    elemento = request.form.get('elemento')  # Recupera il valore dal modulo
    if elemento:
        nuovo_elemento = ListaSpesa(elemento=elemento)  # Crea un nuovo oggetto ListaSpesa
        db.session.add(nuovo_elemento)  # Aggiunge l'oggetto alla sessione del database
        db.session.commit()  # Salva le modifiche nel database
    return redirect(url_for('home'))

# Rotta per registrarsi
@app.route('/registrati', methods=['POST'])
def registrati():
    # Aggiungi logica per registrazione se necessario
    return redirect(url_for('home'))

# Rotta per gestione con immagine bottone
@app.route('/immagine_bottone', methods=['POST'])
def immagine_bottone():
    # Aggiungi logica associata all'azione del bottone immagine
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)  # Avvia l'applicazione Flask in modalità debug
