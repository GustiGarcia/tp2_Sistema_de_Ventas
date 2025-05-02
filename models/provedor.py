from models.db import db

class Proovedor(db.Model):
    __tablename__ = 'proovedor'

    id = db.Column(db.Integer, primary_key=True)
    rut= db.Column(db.String (11), unique= True , nullable=False)
    nombre = db.Column(db.String(25), nullable=False)
    correo = db.Column(db.String(50), unique=True, nullable=False)
    telefono = db.Column(db.String(20), unique=True, nullable=False)
    web= db.column (db.String(30))
    productos = db.relationship('Producto', backref='proovedor', lazy=True)#crea clave foranea

    def __init__(self, rut,nombre, correo, telefono, web):
        self.rut= rut
        self.nombre= nombre
        self.correo = correo
        self.telefono = telefono
        self.web= web


    def serialize(self):
        return {
            'id': self.id,
            'rut':self.rut,
            'nombre': self.nombre,
            'correo': self.correo,
            'telefono': self.telefono,
            'web':self.web
        }    