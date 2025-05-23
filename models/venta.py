from models.db import db
from datetime import datetime

class Venta(db.Model):
    __tablename__='ventas'

    id= db.Column (db.Integer, primary_key=True)
    fecha=db.Column (db.DateTime, default=datetime.now)
    cliente_id=db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    descuento=db.Column(db.Float, nullable=False)
    monto_final=db.Column(db.Float, nullable=False)
    detalles=db.relationship('DetalleVenta', backref='venta', lazy=True)

    def __init__(self, cliente_id, descuento, monto_final, fecha=None):
        self.cliente_id=cliente_id
        self.descuento=descuento
        self.monto_final=monto_final
        if fecha:
            try:
                self.fecha = datetime.strptime(fecha, '%Y-%m-%d') # Intenta convertir la fecha del string
            except ValueError:
                self.fecha = datetime.now() # Si el formato es incorrecto, usa la fecha actual
        else:
            self.fecha = datetime.now()

    def serialize(self):
        return{
            'id':self.id,
            'fecha':self.fecha.strftime('%Y-%m-%d'),
            'cliente_id':self.cliente_id,
            'descuento':self.descuento,
            'monto_final':self.monto_final,
            'detalles':[detalle.serialize() for detalle in self.detalles]
        }