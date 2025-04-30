from flask import Flask
from config.config import DATABASE_CONNECTION_URI
from routes.client_routes import client
from routes.products_routes import products
from models.db import db

app = Flask(__name__)

app.register_blueprint(client)
app.register_blueprint(products)


app.config["SQLALCHEMY_DATABASE_URI"]= DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    from models.client import Client
    from models.products import Products
    # db.drop_all()
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)