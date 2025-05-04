from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from routes.categoria_routes import categoria
from routes.cliente_routes import cliente
from routes.detalleVenta_routes import detalleVenta
from routes.producto_routes import productos
from routes.provedor_routes import provedor
from routes.telefono_routes  import telefono
from routes.venta_routes import ventas
from models.db import db

app = Flask(__name__)

app.register_blueprint(categoria)
app.register_blueprint(cliente)
app.register_blueprint(detalleVenta)
app.register_blueprint(productos)
app.register_blueprint(provedor)
app.register_blueprint(telefono)
app.register_blueprint(ventas)


app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    from models.categoria import Categoria
    from models.cliente import Cliente
    from models.detalleVenta import DetalleVenta
    from models.producto import Producto
    from models.provedor import Provedor
    from models.telefono import Telefono
    from models.venta import Venta
    #db.drop_all() 
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)