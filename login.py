from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurazione del segreto per la gestione delle sessioni
app.config['SECRET_KEY'] = 'your_secret_key'  # Cambia la chiave segreta per sicurezza

# Configurazione database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lista.db'  # URL del database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disabilita il tracciamento delle modifiche

# Inizializza il database
db = SQLAlchemy(app)

# Modello per la lista spesa
class ListaSpesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    elemento = db.Column(db.String(100), nullable=False)

# Modello per gli utenti
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Creazione tabelle nel database
with app.app_context():
    db.create_all()

# Rotta principale (Home)
@app.route('/')
def home():
    # Verifica se l'utente è loggato
    if 'username' in session:
        return render_template('index.html', username=session['username'])  # Home con nome utente
    return redirect(url_for('accedi'))  # Se non loggato, reindirizza alla pagina di login

# Rotta per accedere
@app.route('/accedi', methods=['GET', 'POST'])
def accedi():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = username  # Salva il nome utente nella sessione
            return redirect(url_for('home'))  # Reindirizza alla home dopo il login
        else:
            return "Credenziali errate. Riprova.", 400

    return render_template('accedi.html')  # Renderizza la pagina di login

# Rotta per registrarsi
@app.route('/registrati', methods=['GET', 'POST'])
def registrati():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica se l'utente esiste già
        if User.query.filter_by(username=username).first():
            return "Utente già registrato.", 400

        # Crea il nuovo utente
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('accedi'))  # Redirect alla pagina di login dopo la registrazione

    return render_template('registrati.html')  # Renderizza la pagina di registrazione

# Rotta per la pagina della slot di Book of RA
@app.route('/book_of_ra', methods=['GET', 'POST'])
def book_of_ra():
    if 'username' not in session:
        return redirect(url_for('accedi'))  # Se l'utente non è loggato, lo reindirizza al login
    return render_template('book_of_ra.html')  # Mostra la pagina della slot

# Rotta per la logica dello spin della slot
@app.route('/spin', methods=['GET'])
def spin():
    import random

    # Simboli e logica della slot
    symbols = ["franchino.book_of_ra", "golden_book_of_ra_pharaoh", "book_of_book"]  # Simboli disponibili
    result = random.choices(symbols, k=3)  # Estrae 3 simboli casuali
    is_winner = result[0] == result[1] == result[2]  # Condizione di vincita
    return jsonify({
        "result": result,
        "is_winner": is_winner
    })

# Rotta per fare il logout
@app.route('/logout')
def logout():
    session.pop('username', None)  # Rimuove l'utente dalla sessione
    return redirect(url_for('home'))  # Reindirizza alla home

if __name__ == '__main__':
    app.run(debug=True)  # Avvia l'applicazione Flask in modalità debug
