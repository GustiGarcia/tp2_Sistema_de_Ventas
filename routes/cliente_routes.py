from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from models.db import db
from models.cliente import Cliente
from models.telefono import Telefono

cliente_bp = Blueprint('cliente', __name__)

# Metodo get
@cliente_bp.route('/api/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([cliente.serialize() for cliente in clientes]), 200

# Metodo post
@cliente_bp.route('/api/clientes', methods=['POST'])
def add_cliente():
    data = request.get_json()

    required_fields = ['rut', 'nombre', 'calle', 'numero', 'ciudad', 'provincia']
    if not all(key in data for key in required_fields):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400

    telefonos_data = data.get('telefonos', [])
    if not isinstance(telefonos_data, list):
        return jsonify({'error': 'El campo "telefonos" debe ser una lista'}), 400

    try:
        nuevo_cliente = Cliente(
            rut=data['rut'],
            nombre=data['nombre'],
            calle=data['calle'],
            numero=data['numero'],
            ciudad=data['ciudad'],
            provincia=data['provincia']
        )
        db.session.add(nuevo_cliente)
        db.session.flush()  

        # Crear teléfonos (si los hay)
        telefonos_creados = []
        for numero_tel in telefonos_data:
            nuevo_telefono = Telefono(numero=numero_tel, cliente_id=nuevo_cliente.id)
            db.session.add(nuevo_telefono)
            telefonos_creados.append(nuevo_telefono)

        db.session.commit()  
        return jsonify({
            'mensaje': 'Cliente creado con éxito',
            'cliente': nuevo_cliente.serialize(),
            'telefonos': [tel.serialize() for tel in telefonos_creados] 
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo put remplazando  categorias
@cliente_bp.route('/api/clientes/<int:id>', methods=['PUT'])
def update_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    data = request.get_json()
    try:
        if 'rut' in data:
            cliente.rut = data['rut']
        if 'nombre' in data:
            cliente.nombre = data['nombre']
        if 'calle' in data:
            cliente.calle = data['calle']
        if 'numero' in data:
            cliente.numero = data['numero']
        if 'ciudad' in data:
            cliente.ciudad = data['ciudad']
        if 'provincia' in data:
            cliente.provincia = data['provincia']

        db.session.commit()
        return jsonify({'mensaje': 'Cliente actualizado correctamente', 'cliente': cliente.serialize()}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Metodo patch para actualziar una categoria
@cliente_bp.route('/api/clientes/<int:id>', methods=['PATCH'])
def patch_cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    data = request.get_json()
    try:
        if 'rut' in data:
            cliente.rut = data['rut']
        if 'nombre' in data:
            cliente.nombre = data['nombre']
        if 'calle' in data:
            cliente.calle = data['calle']
        if 'numero' in data:
            cliente.numero = data['numero']
        if 'ciudad' in data:
            cliente.ciudad = data['ciudad']
        if 'provincia' in data:
            cliente.provincia = data['provincia']

        db.session.commit()
        return jsonify({'mensaje': 'Cliente parcialmente actualizado', 'cliente': cliente.serialize()}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo delete para eliminar un cliente
@cliente_bp.route('/api/clientes/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = db.session.get(Cliente, id)
    if not cliente:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    try:
        # Desasociar explícitamente los teléfonos del cliente
        telefonos_a_eliminar = list(cliente.telefono)  # Crear una copia para evitar errores de concurrencia
        for telefono in telefonos_a_eliminar:
            db.session.delete(telefono)

        db.session.delete(cliente)
        db.session.commit()
        return jsonify({'mensaje': 'Cliente y teléfonos eliminados con éxito'}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500