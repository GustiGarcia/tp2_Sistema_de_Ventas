from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.db import db
from models.producto import Producto

productos_bp = Blueprint('productos', __name__)

# Metodo get
@productos_bp.route('/api/productos', methods=['GET'])
def get_productos():
    try:
        productos_all = Producto.query.all()
        productos_serializados = [p.serialize() for p in productos_all]
        return jsonify(productos_serializados), 200
    except SQLAlchemyError as e:
        return jsonify({'error': f'Error al obtener productos: {str(e)}'}), 500

# Metodo post
@productos_bp.route('/api/producto', methods=['POST'])
def create_producto():
    data = request.get_json()
    if not data or 'nombre' not in data or 'precio' not in data or 'stock' not in data or 'provedor_id' not in data or 'categoria_id' not in data:
        return jsonify({'error': 'Faltan campos requeridos: nombre, precio, stock, provedor_id, categoria_id'}), 400

    nombre_producto = data['nombre']

    nuevo_producto = Producto(
        nombre=nombre_producto,
        precio=data['precio'],
        stock=data['stock'],
        provedor_id=data['provedor_id'],
        categoria_id=data['categoria_id']
    )
    try:
        db.session.add(nuevo_producto)
        db.session.commit()
        return jsonify({'mensaje': 'Producto creado con éxito', 'producto': nuevo_producto.serialize()}), 201
    except IntegrityError as e:
        db.session.rollback()
        if "Duplicate entry" in str(e):
            return jsonify({'error': f'Ya existe un producto con el nombre "{nombre_producto}"'}), 400
        return jsonify({'error': str(e)}), 500
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
    if not data or 'nombre' not in data or 'precio' not in data or 'stock' not in data or 'provedor_id' not in data or 'categoria_id' not in data:
        return jsonify({'error': 'Faltan campos requeridos: nombre, precio, stock, provedor_id, categoria_id'}), 400

    try:
        producto.nombre = data['nombre']
        producto.precio = data['precio']
        producto.stock = data['stock']
        producto.provedor_id = data['provedor_id']
        producto.categoria_id = data['categoria_id']
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
        if 'provedor_id' in data:
            producto.provedor_id = data['provedor_id']
        if 'categoria_id' in data:
            producto.categoria_id = data['categoria_id']
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
