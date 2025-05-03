from models.db import db

class DetalleVenta(db.Model):
    __tablename__= 'detalle_venta'
    id= db.Column (db.Integer, primary_key=True)
    venta_id=db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    producto_id=db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad= db.Column(db.Integer, nullable=False)
    precio_unitario=db.Column(db.Float, nullable=False)
    subtotal=db.Column (db.Float, nullable=False)

    def __init__(self, venta_id, producto_id, cantidad, precio_unitario):
        self.venta_id = venta_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.subtotal = cantidad * precio_unitario  # Lo calculamos automáticamente al crear

    def serialize(self):
        return {
            'id': self.id,
            'venta_id': self.venta_id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.subtotal
        }