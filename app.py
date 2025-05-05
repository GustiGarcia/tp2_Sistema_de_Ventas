from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from routes.categoria_routes import categoria_bp
from routes.cliente_routes import cliente_bp
from routes.detalleVenta_routes import detalle_ventas_bp
from routes.producto_routes import productos_bp
from routes.provedor_routes import provedor_bp
from routes.telefono_routes  import telefono_bp
from routes.venta_routes import ventas_bp
from models.db import db

app = Flask(__name__)

app.register_blueprint(categoria_bp) 
app.register_blueprint(cliente_bp)
app.register_blueprint(detalle_ventas_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(provedor_bp)
app.register_blueprint(telefono_bp)
app.register_blueprint(ventas_bp)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
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
