from flask_sqlalchemy import SQLAlchemy #import sqlAlchemy
db = SQLAlchemy() #inizializza db 
class ListaSpesa(db.Model):#creazione classe lista 
    id = db.Column(db.Integer, primary_key=True) # definisci la colonna id come chiave primaria intera
    elemento = db.Column(db.String(100), nullable=False) # definisce la colonna elemento come stringa non nulla 