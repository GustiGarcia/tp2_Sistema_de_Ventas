from flask import Blueprint, jsonify
from models.products import Products

products = Blueprint('products', __name__)

@products.route('/api/products')
def get_products():
    products = Products.query.all()
    return jsonify([product.serialize() for product in products])