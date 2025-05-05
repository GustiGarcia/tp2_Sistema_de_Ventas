from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from models.db import db
from models.venta import Venta
from models.cliente import Cliente

ventas = Blueprint('ventas', __name__)

# Metodo get
@ventas.route('/api/ventas', methods=['GET'])
def get_ventas():
    ventas_all = Venta.query.all()
    return jsonify([v.serialize() for v in ventas_all]), 200

# Metodo post (crea una venta)
@ventas.route('/api/venta', methods=['POST'])
def create_venta():
    data = request.get_json()

    if not data or 'cliente_id' not in data or 'fecha' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    cliente = Cliente.query.get(data['cliente_id'])
    if not cliente:
        return jsonify({'error': 'Cliente no existente'}), 404

    nueva_venta = Venta(
        cliente_id=data['cliente_id'],
        fecha=data['fecha']
    )

    try:
        db.session.add(nueva_venta)
        db.session.commit()
        return jsonify({'mensaje': 'Venta creada', 'venta': nueva_venta.serialize()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo put (actualzia una venta completamente)
@ventas.route('/api/venta/<int:id>', methods=['PUT'])
def update_venta(id):
    venta = Venta.query.get(id)
    if not venta:
        return jsonify({'error': 'Venta no encontrada'}), 404

    data = request.get_json()
    if not data or 'cliente_id' not in data or 'fecha' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    cliente = Cliente.query.get(data['cliente_id'])
    if not cliente:
        return jsonify({'error': 'Cliente no existente'}), 404

    try:
        venta.cliente_id = data['cliente_id']
        venta.fecha = data['fecha']
        db.session.commit()
        return jsonify({'mensaje': 'Venta actualizada', 'venta': venta.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo patch (actualzia momentaneamente una venta)
@ventas.route('/api/venta/<int:id>', methods=['PATCH'])
def patch_venta(id):
    venta = Venta.query.get(id)
    if not venta:
        return jsonify({'error': 'Venta no encontrada'}), 404

    data = request.get_json()

    try:
        if 'cliente_id' in data:
            cliente = Cliente.query.get(data['cliente_id'])
            if not cliente:
                return jsonify({'error': 'Cliente no existente'}), 404
            venta.cliente_id = data['cliente_id']
        if 'fecha' in data:
            venta.fecha = data['fecha']
        db.session.commit()
        return jsonify({'mensaje': 'Venta actualizada parcialmente', 'venta': venta.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo delete (Eliminamos venta)
@ventas.route('/api/venta/<int:id>', methods=['DELETE'])
def delete_venta(id):
    venta = Venta.query.get(id)
    if not venta:
        return jsonify({'error': 'Venta no encontrada'}), 404

    try:
        db.session.delete(venta)
        db.session.commit()
        return jsonify({'mensaje': 'Venta eliminada', 'venta': venta.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
