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

    if not data or 'cliente_id' not in data or 'descuento' not in data or 'monto_final' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    cliente = Cliente.query.get(data['cliente_id'])
    if not cliente:
        return jsonify({'error': 'Cliente no existente'}), 404
    
    descuento = data['descuento']
    monto_final= data['monto_final']

    if descuento < 0:
        return jsonify({'error': 'El descuento no puede ser negativo'}),400
    if descuento > 0.30:
        return jsonify({'error': 'El descuento no puede ser mayor a 30%'}),400
    if monto_final < 0:
        return jsonify({'error' : 'El monto total no puede ser menor a 0'}),400
    
    monto_final = monto_final - (monto_final*descuento)

    nueva_venta = Venta(
        cliente_id=data['cliente_id'],
        descuento=data['descuento'],
        monto_final=monto_final
        
    )

    try:
        db.session.add(nueva_venta)
        db.session.commit()
        return jsonify({'mensaje': 'Venta creada', 'venta': nueva_venta.serialize()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo put (actualzia una venta completamente)
@ventas_bp.route('/api/venta/<int:id>', methods=['PUT'])
def update_venta(id):
    venta = Venta.query.get(id)
    if not venta:
        return jsonify({'error': 'Venta no encontrada'}), 404

    data = request.get_json()
    
    if not data or 'cliente_id' not in data or 'descuento' not in data or 'monto_final' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400
    cliente = Cliente.query.get(data['cliente_id'])
    if not cliente:
        return jsonify({'error': 'Cliente no existente'}), 404
    
    
    descuento = data['descuento']
    monto_final= data['monto_final']

    if descuento < 0:
        return jsonify({'error': 'El descuento no puede ser negativo'}),400
    if descuento > 0.30:
        return jsonify({'error': 'El descuento no puede ser mayor a 30%'}),400
    if monto_final < 0:
        return jsonify({'error' : 'El monto total no puede ser menor a 0'}),400
    
    monto_final = monto_final - (monto_final*descuento)

    try:
        venta.cliente_id = data['cliente_id']
        venta.descuento = data['descuento']
        venta.monto_final=monto_final
        db.session.commit()
        return jsonify({'mensaje': 'Venta actualizada', 'venta': venta.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo patch (actualzia momentaneamente una venta)
@ventas_bp.route('/api/venta/<int:id>', methods=['PATCH'])
def patch_venta(id):
    venta = Venta.query.get(id)
    if not venta:
        return jsonify({'error': 'Venta no encontrada'}), 404

    data = request.get_json()

    try:
        # Si llega cliente_id → validar cliente existente
        if 'cliente_id' in data:
            cliente = Cliente.query.get(data['cliente_id'])
            if not cliente:
                return jsonify({'error': 'Cliente no existente'}), 404
            venta.cliente_id = data['cliente_id']

        # Si llega fecha
        if 'fecha' in data:
            venta.fecha = data['fecha']

        # Si llega descuento → validar
        if 'descuento' in data:
            descuento = data['descuento']
            if descuento < 0:
                return jsonify({'error': 'El descuento no puede ser negativo'}), 400
            if descuento > 0.30:
                return jsonify({'error': 'El descuento no puede ser mayor a 30%'}), 400
            venta.descuento = descuento

        # Si llega monto_final → validar
        if 'monto_final' in data:
            monto_final = data['monto_final']
            if monto_final < 0:
                return jsonify({'error': 'El monto total no puede ser menor a 0'}), 400
            venta.monto_final = monto_final

        # Asegurarse de recalcular siempre el monto final con descuento actualizado
        venta.monto_final = venta.monto_final - (venta.monto_final * venta.descuento)

        db.session.commit()
        return jsonify({'mensaje': 'Venta actualizada parcialmente', 'venta': venta.serialize()}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo delete (Eliminamos venta)
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
