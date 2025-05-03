from models.db import db

class Cliente(db.Model):
    __tablename__='clientes'
    id=db.Column (db.Integer, primary_key=True)
    rut=db.Column(db.String(11), unique=True,nullable=False)
    nombre=db.Column(db.String(30), nullable=False)
    calle=db.Column (db.String(25), nullable=False)
    numero=db.Column(db.String(8), nullable=False)
    ciudad=db.Column(db.String(20), nullable=False)
    provincia=db.Column(db.String(20), nullable=False)
    telefono=db.relationship('Telefono', backref='cliente', lazy=True)

    def __init__(self,rut,nombre,calle,numero,ciudad,provincia):
        self.rut=rut
        self.nombre=nombre
        self.calle=calle
        self.numero=numero
        self.ciudad=ciudad
        self.provincia=provincia

    
    def serialize(self):
        return{
        'id': self.id,
        'rut': self.rut,
        'nombre': self.nombre,
        'calle': self.calle,
        'numero': self.numero,
        'ciudad': self.ciudad,
        'provincia': self.provincia,
        'telefonos': [tel.numero for tel in self.telefono]
        }