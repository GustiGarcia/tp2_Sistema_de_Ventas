from flask import Blueprint, jsonify, request
from models.producto import Producto

productos = Blueprint('productos', __name__)

@productos.route('/api/productos')
def get_products():
    productos = Producto.query.all()
    return jsonify([product.serialize() for product in productos])