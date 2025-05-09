from models.db import db
from sqlalchemy import ForeignKey

class Telefono(db.Model):
    __tablename__='telefonos'
    id=db.Column(db.Integer,primary_key=True)#agregar id para cada telefono
    numero=db.Column(db.String(15),nullable=False)
    cliente_id=db.Column(db.Integer, db.ForeignKey('clientes.id',ondelete='CASCADE'), nullable=False)
    

    def __init__(self,numero, cliente_id):
        self.numero=numero
        self.cliente_id=cliente_id     

    def serialize(self):
        return{
            'id':self.id,
            'numero':self.numero,
            'cliente_id':self.cliente_id
        }
