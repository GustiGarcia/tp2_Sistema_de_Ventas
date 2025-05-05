from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from models.db import db
from models.provedor import Provedor

provedor = Blueprint('provedor', __name__)

# Metodo get
@provedor.route('/api/provedores', methods=['GET'])
def get_provedores():
    provedores = Provedor.query.all()
    return jsonify([p.serialize() for p in provedores]), 200

# Metodo post
@provedor.route('/api/provedor', methods=['POST'])
def create_provedor():
    data = request.get_json()
    
    if not data or 'nombre' not in data or 'contacto' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    nuevo = Provedor(nombre=data['nombre'], contacto=data['contacto'])

    try:
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({'mensaje': 'Proveedor creado', 'provedor': nuevo.serialize()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# metodo put
@provedor.route('/api/provedor/<int:id>', methods=['PUT'])
def update_provedor(id):
    prov = Provedor.query.get(id)
    if not prov:
        return jsonify({'error': 'Proveedor no encontrado'}), 404

    data = request.get_json()
    if not data or 'nombre' not in data or 'contacto' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    try:
        prov.nombre = data['nombre']
        prov.contacto = data['contacto']
        db.session.commit()
        return jsonify({'mensaje': 'Proveedor actualizado', 'provedor': prov.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Metodo patch
@provedor.route('/api/provedor/<int:id>', methods=['PATCH'])
def patch_provedor(id):
    prov = Provedor.query.get(id)
    if not prov:
        return jsonify({'error': 'Proveedor no encontrado'}), 404

    data = request.get_json()
    try:
        if 'nombre' in data:
            prov.nombre = data['nombre']
        if 'contacto' in data:
            prov.contacto = data['contacto']
        db.session.commit()
        return jsonify({'mensaje': 'Proveedor actualizado parcialmente', 'provedor': prov.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Metodo delete
@provedor.route('/api/provedor/<int:id>', methods=['DELETE'])
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
