from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key=True)          # ID producto
    nombre = db.Column(db.String(120), nullable=False)    # nombre del producto
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)

class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)          # ID cliente
    nombre = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=True)
