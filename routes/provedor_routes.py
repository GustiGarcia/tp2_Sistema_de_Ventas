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
    required_fields = ['rut', 'nombre', 'correo', 'telefono', 'web']

    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos'}), 400


    nuevo = Provedor(rut=data['rut'],nombre=data['nombre'],correo=data['correo'] ,telefono=data['telefono'], web=data['web'])

    try:
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({'mensaje': 'Proveedor creado', 'provedor': nuevo.serialize()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# metodo put
@provedor_bp.route('/api/provedor/<int:id>', methods=['PUT'])
def update_provedor(id):
    prov = Provedor.query.get(id)
    if not prov:
        return jsonify({'error': 'Proveedor no encontrado'}), 404

    data = request.get_json()
    required_fields = ['rut', 'nombre', 'correo', 'telefono', 'web']

    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Faltan campos requeridos'}), 400


    try:
        prov.rut=data['rut']
        prov.nombre = data['nombre']
        prov.correo=data['correo']
        prov.telefono = data['telefono']
        prov.web=data['web']
        db.session.commit()
        return jsonify({'mensaje': 'Proveedor actualizado', 'provedor': prov.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Metodo patch
@provedor_bp.route('/api/provedor/<int:id>', methods=['PATCH'])
def patch_provedor(id):
    prov = Provedor.query.get(id)
    if not prov:
        return jsonify({'error': 'Proveedor no encontrado'}), 404

    data = request.get_json()
    try:
        if 'rut' in data:
            prov.rut=data['rut']
        if 'nombre' in data:
            prov.nombre = data['nombre']
        if 'correo' in data:
            prov.correo=data['correo']
        if 'telefono' in data:
            prov.telefono = data['telefono']
        if 'web' in data:
            prov.web=data['web']

        db.session.commit()
        return jsonify({'mensaje': 'Proveedor actualizado parcialmente', 'provedor': prov.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Metodo delete
@provedor_bp.route('/api/provedor/<int:id>', methods=['DELETE'])
def delete_provedor(id):
    prov = Provedor.query.get(id)
    if not prov:
        return jsonify({'error': 'Proveedor no encontrado'}), 404

    try:
        db.session.delete(prov)
        db.session.commit()
        return jsonify({'mensaje': 'Proveedor eliminado', 'provedor': prov.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
