from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import re  # Import necessario per `verifica_password`

app = Flask(__name__)

# Configurazione del segreto per la gestione delle sessioni
app.config['SECRET_KEY'] = 'your_secret_key'  # Cambia questa chiave per sicurezza

# Configurazione database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lista.db'  # URL del database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disabilita il tracciamento delle modifiche

# Inizializza il database
db = SQLAlchemy(app)

# Modello per la lista spesa
class ListaSpesa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    elemento = db.Column(db.String(100), unique=True, nullable=False)

# Modello per gli utenti
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Creazione tabelle nel database
with app.app_context():
    db.create_all()

# Funzione per verificare la sicurezza della password
def verifica_password(password):
    # Lunghezza minima
    if len(password) < 8:
        return "La password deve contenere almeno 8 caratteri."
    # Almeno una lettera maiuscola
    if not re.search(r"[A-Z]", password):
        return "La password deve contenere almeno una lettera maiuscola."
    # Almeno una lettera minuscola
    if not re.search(r"[a-z]", password):
        return "La password deve contenere almeno una lettera minuscola."
    # Almeno un numero
    if not re.search(r"[0-9]", password):
        return "La password deve contenere almeno un numero."
    # Almeno un carattere speciale
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "La password deve contenere almeno un carattere speciale."
    return "Password valida!"

# Rotta principale (Home)
@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('accedi'))

# Rotta per accedere
@app.route('/accedi', methods=['GET', 'POST'])
def accedi():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['username'] = username
            return redirect(url_for('home'))
        return "Credenziali errate. Riprova.", 400
    return render_template('accedi.html')

# Rotta per registrarsi
@app.route('/registrati', methods=['GET', 'POST'])
def registrati():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica se l'utente esiste già
        if User.query.filter_by(username=username).first():
            return "Utente già registrato.", 400

        # Validazione della password
        verifica = verifica_password(password)
        if verifica != "Password valida!":
            return verifica, 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('accedi'))
    return render_template('registrati.html')

# Rotta per la pagina della slot di Book of RA
@app.route('/book_of_ra')
def book_of_ra():
    if 'username' not in session:
        return redirect(url_for('accedi'))
    return render_template('book_of_ra.html')

# Rotta per la logica dello spin della slot
@app.route('/spin', methods=['POST'])
def spin():
    import random
    symbols = ["franchino.book_of_ra", "golden_book_of_ra_pharaoh", "book_of_ra_deluxe_book"]
    result = random.choices(symbols, k=3)
    is_winner = result[0] == result[1] == result[2]
    return jsonify({"result": result, "is_winner": is_winner})

# Rotta per fare il logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
