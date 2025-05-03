from models.db import db
from datetime  import datetime

class Venta(db.Model):
    __tablename__='ventas'
    
    id= db.Column (db.Integer, primary_key=True)
    fecha=db.Column (db.DateTime, default=datetime.now)
    cliente_id=db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    descuento=db.Column(db.Float, nullable=False)
    monto_final=db.Column(db.Float, nullable=False)
    detalles=db.relationship('DetalleVenta', backref='venta', lazy=True)

    def __init__(self,  cliente_id, descuento, monto_final):
        self.cliente_id=cliente_id
        self.descuento=descuento
        self.monto_final=monto_final
    
    def serialize(self):
        return{
            'id':self.id,
            'fecha':self.fecha.strftime('%Y-%m-%d'),
            'cliente_id':self.cliente_id,
            'descuento':self.descuento,
            'monto_final':self.monto_final,
            'detalles':[detalle.serialize() for detalle in self.detalles]
        }
