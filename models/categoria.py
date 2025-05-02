from models.db import db

class Categoria(db.Model):
    __tablename__='categoria'
    
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(20), unique=True, nullable=False)
    descripcion=db.Column(db.String(60), nullable=False)
    categoria_rel=db.relationship('productos', backref='Categoria', lazy = True)

"""    categoria_id=db.Column(db.Integer,db.ForeignKey(''))

    def __init__(self,id,nombre,descripcion):
        self.id=id
        self.nombre=nombre
        self.descripcion=descripcion

    def serialize(self):
        return{
            'id':self.id,
            'nombre':self.nombre,
            'descripcion':self.descripcion
        }"""