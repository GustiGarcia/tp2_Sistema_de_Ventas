from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from models.db import db
from models.detalleVenta import DetalleVenta
from models.venta import Venta
from models.producto import Producto

detalle_ventas_bp = Blueprint('detalle_ventas', __name__)

# Metodo get
@detalle_ventas_bp.route('/api/detalles-venta', methods=['GET'])
def get_detalles_venta():
    detalles = DetalleVenta.query.all()
    return jsonify([d.serialize() for d in detalles]), 200

# Metodo post (Crea detalle)
@detalle_ventas_bp.route('/api/detalle-venta', methods=['POST'])
def create_detalle_venta():
    data = request.get_json()

    if not data or 'venta_id' not in data or 'producto_id' not in data or 'cantidad' not in data or 'precio_unitario' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    # Verifica productos
    venta = Venta.query.get(data['venta_id'])
    producto = Producto.query.get(data['producto_id'])
    if not venta or not producto:
        return jsonify({'error': 'Venta o Producto no existente'}), 404
    
    nuevo_detalle = DetalleVenta(
        venta_id=data['venta_id'],
        producto_id=data['producto_id'],
        cantidad=data['cantidad'],
        precio_unitario=data['precio_unitario']
    )

    try:
        db.session.add(nuevo_detalle)
        db.session.commit()
        return jsonify({'mensaje': 'Detalle de venta creado', 'detalle': nuevo_detalle.serialize()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo put
@detalle_ventas_bp.route('/api/detalle-venta/<int:id>', methods=['PUT'])
def update_detalle_venta(id):
    detalle = DetalleVenta.query.get(id)
    if not detalle:
        return jsonify({'error': 'Detalle no encontrado'}), 404

    data = request.get_json()
    if not data or 'venta_id' not in data or 'producto_id' not in data or 'cantidad' not in data or 'precio_unitario' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    venta = Venta.query.get(data['venta_id'])
    producto = Producto.query.get(data['producto_id'])

    if not venta or not producto:
        return jsonify({'error': 'Venta o Producto no existente'}), 404

    try:
        detalle.venta_id = data['venta_id']
        detalle.producto_id = data['producto_id']
        detalle.cantidad = data['cantidad']
        db.session.commit()
        return jsonify({'mensaje': 'Detalle actualizado', 'detalle': detalle.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo path (actualizaciones)
@detalle_ventas_bp.route('/api/detalle-venta/<int:id>', methods=['PATCH'])
def patch_detalle_venta(id):
    detalle = DetalleVenta.query.get(id)
    if not detalle:
        return jsonify({'error': 'Detalle no encontrado'}), 404

    data = request.get_json()

    try:
        if 'venta_id' in data:
            venta = Venta.query.get(data['venta_id'])
            if not venta:
                return jsonify({'error': 'Venta no existente'}), 404
            detalle.venta_id = data['venta_id']
        if 'producto_id' in data:
            producto = Producto.query.get(data['producto_id'])
            if not producto:
                return jsonify({'error': 'Producto no existente'}), 404
            detalle.producto_id = data['producto_id']
        if 'cantidad' in data:
            detalle.cantidad = data['cantidad']
        if 'precio_unitario' in data:
            detalle.precio_unitario=data['precio_unitario']
        if 'subtotal' in data:
            detalle.subtotal=data['subtotal']
        db.session.commit()
        return jsonify({'mensaje': 'Detalle actualizado parcialmente', 'detalle': detalle.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo delete (elimina detalle)
@detalle_ventas_bp.route('/api/detalle-venta/<int:id>', methods=['DELETE'])
def delete_detalle_venta(id):
    detalle = DetalleVenta.query.get(id)
    if not detalle:
        return jsonify({'error': 'Detalle no encontrado'}), 404

    try:
        db.session.delete(detalle)
        db.session.commit()
        return jsonify({'mensaje': 'Detalle eliminado', 'detalle': detalle.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
