from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from models.db import db
from models.provedor import Provedor

provedor_bp = Blueprint('provedor', __name__)

# Metodo get
@provedor_bp.route('/api/provedores', methods=['GET'])
def get_provedores():
    provedores = Provedor.query.all()
    return jsonify([p.serialize() for p in provedores]), 200

# Metodo post
@provedor_bp.route('/api/provedor', methods=['POST'])
def create_provedor():
    data = request.get_json()
    if not data or 'nombre' not in data:
        return jsonify({'error': 'Falta el campo requerido: nombre'}), 400

    nuevo_provedor = Provedor(
        nombre=data['nombre'],
        rut=data.get('rut'),
        correo=data.get('correo'),
        telefono=data.get('telefono'),
        web=data.get('web')
    )
    try:
        db.session.add(nuevo_provedor)
        db.session.commit()
        return jsonify({'mensaje': 'Proveedor creado con éxito', 'proveedor': nuevo_provedor.serialize()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo put
@provedor_bp.route('/api/provedor/<int:id>', methods=['PUT'])
def update_provedor(id):
    proveedor = Provedor.query.get(id)
    if not proveedor:
        return jsonify({'error': 'Proveedor no encontrado'}), 404

    data = request.get_json()
    if not data or 'nombre' not in data: 
        return jsonify({'error': 'Falta el campo requerido: nombre'}), 400

    try:
        proveedor.nombre = data['nombre']
        proveedor.rut = data.get('rut')
        proveedor.correo = data.get('correo')
        proveedor.telefono = data.get('telefono')
        proveedor.web = data.get('web')
        db.session.commit()
        return jsonify({'mensaje': 'Proveedor actualizado con éxito', 'proveedor': proveedor.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo patch
@provedor_bp.route('/api/provedor/<int:id>', methods=['PATCH'])
def patch_provedor(id):
    proveedor = Provedor.query.get(id)
    if not proveedor:
        return jsonify({'error': 'Proveedor no encontrado'}), 404

    data = request.get_json()
    try:
        if 'nombre' in data:
            proveedor.nombre = data['nombre']
        if 'rut' in data:
            proveedor.rut = data['rut']
        if 'correo' in data:
            proveedor.correo = data['correo']
        if 'telefono' in data:
            proveedor.telefono = data['telefono']
        if 'web' in data:
            proveedor.web = data['web']
        db.session.commit()
        return jsonify({'mensaje': 'Proveedor actualizado parcialmente', 'proveedor': proveedor.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo delete
@provedor_bp.route('/api/provedor/<int:id>', methods=['DELETE'])
def delete_provedor(id):
    proveedor = Provedor.query.get(id)
    if not proveedor:
        return jsonify({'error': 'Proveedor no encontrado'}), 404

    try:
        db.session.delete(proveedor)
        db.session.commit()
        return jsonify({'mensaje': 'Proveedor eliminado con éxito', 'proveedor': proveedor.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
