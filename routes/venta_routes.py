from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from models.db import db
from models.venta import Venta
from models.cliente import Cliente

ventas_bp = Blueprint('ventas', __name__)

# Metodo get
@ventas_bp.route('/api/ventas', methods=['GET'])
def get_ventas():
    ventas_all = Venta.query.all()
    return jsonify([v.serialize() for v in ventas_all]), 200

# Metodo post (crea una venta)
@ventas_bp.route('/api/venta', methods=['POST'])
def create_venta():
    data = request.get_json()

    if not data or 'cliente_id' not in data or 'fecha' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    cliente = Cliente.query.get(data['cliente_id'])
    if not cliente:
        return jsonify({'error': 'Cliente no existente'}), 404

    nueva_venta = Venta(
        cliente_id=data['cliente_id'],
        descuento=data.get('descuento'),
        monto_final=data.get('monto_final'),
        fecha=data['fecha']
    )

    try:
        db.session.add(nueva_venta)
        db.session.commit()
        return jsonify({'mensaje': 'Venta creada', 'venta': nueva_venta.serialize()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo put (actualiza una venta completamente)
@ventas_bp.route('/api/venta/<int:id>', methods=['PUT'])
def update_venta(id):
    venta = Venta.query.get(id)
    if not venta:
        return jsonify({'error': 'Venta no encontrada'}), 404

    data = request.get_json()
    if not data or 'cliente_id' not in data or 'fecha' not in data or 'descuento' not in data or 'monto_final' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400 # Añadí validación para descuento y monto_final

    cliente = Cliente.query.get(data['cliente_id'])
    if not cliente:
        return jsonify({'error': 'Cliente no existente'}), 404

    try:
        venta.cliente_id = data['cliente_id']
        venta.fecha = data['fecha']
        venta.descuento = data['descuento'] # Actualiza el descuento
        venta.monto_final = data['monto_final'] # Actualiza el monto_final
        db.session.commit()
        return jsonify({'mensaje': 'Venta actualizada', 'venta': venta.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo patch (actualiza momentaneamente una venta)
@ventas_bp.route('/api/venta/<int:id>', methods=['PATCH'])
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
        if 'descuento' in data: # Agregado para actualizar descuento
            venta.descuento = data['descuento']
        if 'monto_final' in data: # Agregado para actualizar monto_final
            venta.monto_final = data['monto_final']
        db.session.commit()
        return jsonify({'mensaje': 'Venta actualizada parcialmente', 'venta': venta.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo delete (Elimina una venta)
@ventas_bp.route('/api/venta/<int:id>', methods=['DELETE'])
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
