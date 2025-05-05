from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from models.db import db
from models.producto import Producto

productos_bp = Blueprint('productos', __name__)

# Metodo get
@productos_bp.route('/api/productos', methods=['GET'])
def get_productos():
    productos_all = Producto.query.all()
    return jsonify([p.serialize() for p in productos_all]), 200

# Metodo post
@productos_bp.route('/api/producto', methods=['POST'])
def create_producto():
    data = request.get_json()
    if not data or 'nombre' not in data or 'precio' not in data or 'stock' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    nuevo_producto = Producto(
        nombre=data['nombre'],
        precio=data['precio'],
        stock=data['stock']
    )
    try:
        db.session.add(nuevo_producto)
        db.session.commit()
        return jsonify({'mensaje': 'Producto creado con éxito', 'producto': nuevo_producto.serialize()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo put
@productos_bp.route('/api/producto/<int:id>', methods=['PUT'])
def update_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    data = request.get_json()
    if not data or 'nombre' not in data or 'precio' not in data or 'stock' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    try:
        producto.nombre = data['nombre']
        producto.precio = data['precio']
        producto.stock = data['stock']
        db.session.commit()
        return jsonify({'mensaje': 'Producto actualizado', 'producto': producto.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo patch
@productos_bp.route('/api/producto/<int:id>', methods=['PATCH'])
def patch_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    data = request.get_json()
    try:
        if 'nombre' in data:
            producto.nombre = data['nombre']
        if 'precio' in data:
            producto.precio = data['precio']
        if 'stock' in data:
            producto.stock = data['stock']
        db.session.commit()
        return jsonify({'mensaje': 'Producto actualizado parcialmente', 'producto': producto.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo delete
@productos_bp.route('/api/producto/<int:id>', methods=['DELETE'])
def delete_producto(id):
    producto = Producto.query.get(id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    try:
        db.session.delete(producto)
        db.session.commit()
        return jsonify({'mensaje': 'Producto eliminado', 'producto': producto.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
