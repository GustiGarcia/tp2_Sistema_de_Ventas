from flask import Blueprint, jsonify, request
from models.db import db
from models.telefono import Telefono
from sqlalchemy.exc import SQLAlchemyError

telefono = Blueprint('telefono', __name__)

# GET - obtener todos los teléfonos
@telefono.route('/api/telefonos', methods=['GET'])
def get_telefonos():
    telefonos_clientes = Telefono.query.all()
    return jsonify([t.serialize() for t in telefonos_clientes]), 200


# POST - crear un nuevo teléfono
@telefono.route('/api/telefono', methods=['POST'])
def create_telefono():
    data = request.get_json()

    if not data or 'numero' not in data or 'cliente_id' not in data:
        return jsonify({'error': 'Faltan campos requeridos'}), 400

    nuevo_telefono = Telefono(numero=data['numero'], cliente_id=data['cliente_id'])

    try:
        db.session.add(nuevo_telefono)
        db.session.commit()
        return jsonify({'mensaje': 'Teléfono creado', 'telefono': nuevo_telefono.serialize()}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# PUT - actualizar completamente un teléfono
@telefono.route('/api/telefono/<int:id>', methods=['PUT'])
def update_telefono(id):
    telefono_obj = Telefono.query.get(id)
    if not telefono_obj:
        return jsonify({'error': 'Teléfono no encontrado'}), 404

    data = request.get_json()
    if not data or 'numero' not in data or 'cliente_id' not in data:
        return jsonify({'error': 'Faltan campos para actualizar'}), 400

    try:
        telefono_obj.numero = data['numero']
        telefono_obj.cliente_id = data['cliente_id']
        db.session.commit()
        return jsonify({'mensaje': 'Teléfono actualizado', 'telefono': telefono_obj.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# PATCH - actualizar parcialmente un teléfono
@telefono.route('/api/telefono/<int:id>', methods=['PATCH'])
def patch_telefono(id):
    telefono_obj = Telefono.query.get(id)
    if not telefono_obj:
        return jsonify({'error': 'Teléfono no encontrado'}), 404

    data = request.get_json()
    try:
        if 'numero' in data:
            telefono_obj.numero = data['numero']
        if 'cliente_id' in data:
            telefono_obj.cliente_id = data['cliente_id']

        db.session.commit()
        return jsonify({'mensaje': 'Teléfono actualizado parcialmente', 'telefono': telefono_obj.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# DELETE - eliminar un teléfono
@telefono.route('/api/telefono/<int:id>', methods=['DELETE'])
def delete_telefono(id):
    telefono_obj = Telefono.query.get(id)
    if not telefono_obj:
        return jsonify({'error': 'Teléfono no encontrado'}), 404

    try:
        db.session.delete(telefono_obj)
        db.session.commit()
        return jsonify({'mensaje': 'Teléfono eliminado', 'telefono': telefono_obj.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
