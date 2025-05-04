from models.db import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), unique=True, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    provedor_id= db.Column(db.Integer, db.ForeignKey('provedor.id'), nullable=False)
    categoria_id= db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

def __init__(self, nombre, precio, stock, proovedor_id, categoria_id):
    self.nombre = nombre
    self.precio = precio
    self.stock = stock
    self.proovedor_id = proovedor_id
    self.categoria_id = categoria_id


def serialize(self):
    return {
        'id': self.id,
        'nombre': self.nombre,
        'precio': self.precio,
        'stock': self.stock,
        'proovedor_id': self.provedor_id,
        'categoria_id': self.categoria_id
    }
