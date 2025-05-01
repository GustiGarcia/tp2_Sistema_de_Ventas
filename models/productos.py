from models.db import db

class Producto(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60), unique=True, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    proovedor_id= db.Column(db.Integer, dbForeignKey('proovedor.id'), nullable=False)
    categoria_id= db.Column (db.Integer, dbForeignKey('categoria.id'), nullable=False)
    proovedor= db.relationship ('Proovedor', backreef='productos', lazy =True)
    categoria= db.relationship('Categoria', backreef='productos' lazy=True)
    

   def __init__(self, nombre, precio_actual, stock_disponible, proveedor_id, categoria_id):
        self.nombre = nombre
        self.precio_actual = precio_actual
        self.stock_disponible = stock_disponible
        self.proveedor_id = proveedor_id
        self.categoria_id = categoria_id

     def __repr__(self):
        return f"<Producto {self.nombre}>"

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio_actual': str(self.precio_actual), # Convertir Numeric a string para JSON
            'stock_disponible': self.stock_disponible,
            'proveedor_id': self.proveedor_id,
            'categoria_id': self.categoria_id
            # Podrías incluir información del proveedor y categoría si lo deseas
            # 'proveedor': self.proveedor.nombre if self.proveedor else None,
            # 'categoria': self.categoria.nombre if self.categoria else None
        }