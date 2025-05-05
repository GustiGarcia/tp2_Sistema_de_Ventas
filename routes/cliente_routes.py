from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.cliente import Cliente
from models.telefono import Telefono

cliente = Blueprint('cliente', __name__)

@cliente.route('/api/clientes', methods=['GET'])
def get_clientes():
    clientes = Cliente.query.all()
    return jsonify([cliente.serialize() for cliente in clientes])


@cliente.route('/api/cliente', methods=['POST'])
def add_client():
    data = request.get_json()

    if not data or not all(key in data for key in ['rut','nombre','calle','numero','ciudad','provincia']):
        return jsonify({'Error': 'faltan datos '}),400

    telefonos_data = data.get('telefonos', [])
    if not isinstance(telefonos_data, list):
        return jsonify({'Error': 'El campo telefonos debe ser una lista'}),400

    nuevo_cliente = Cliente(
        rut=data['rut'],
        nombre=data['nombre'],
        calle=data['calle'],
        numero=data['numero'],
        ciudad=data['ciudad'],
        provincia=data['provincia']
    )
    db.session.add(nuevo_cliente)
    db.session.commit()  # Ahora ya tiene ID

    # Crear teléfonos (si los hay)
    for numero_tel in telefonos_data:
        nuevo_telefono = Telefono(numero=numero_tel, cliente_id=nuevo_cliente.id)
        db.session.add(nuevo_telefono)

    db.session.commit()

    return jsonify({
        'mensaje': 'Cliente creado con éxito',
        'cliente': nuevo_cliente.serialize()
    }), 201

    
"""

@cliente.route("/api/del_client/<int:id>", methods=['DELETE'])
def delete_client(id):
    cliente = Cliente.query.get(id)
    
    if not cliente: 
        return jsonify({'message':'Cliente not found'}), 404 
    try:
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({'message': 'Client delete successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':str(e)}), 500

@cliente.route('/api/up_client/<int:id>', methods=['PUT'])
def update_cliente(id):

    data = request.get_json()

    if not data:
        return jsonify({'error':'No se recibieron datos'}, 400)
    
    client = Cliente.query.get(id)

    if not client:
        return jsonify({'error': 'Cliente no encontrado'}), 404
    
    try:
        if "name" in data:
            client.name = data['name']
        if 'email' in data:
            client.email = data['email']
        if 'phone' in data:
            client.phone = data['phone']

        db.session.commit()

        return jsonify({'message':'Cliente actulizado correctamente', 'client': client.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

@cliente.route('/api/update_client/<int:id>', methods=['PATCH'])
def patch_client(id):
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No se recibieron datos'}), 400

    client = Cliente.query.get(id)
    
    if not client:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    try:
        if 'name' in data and data['name']:
            client.name = data['name']
        if 'email' in data and data['email']:
            client.email = data['email']
        if 'phone' in data and data['phone']:
            client.phone = data['phone']

        db.session.commit()
        return jsonify({'message': 'Cliente actualizado correctamente', 'client': client.serialize()}), 200

   
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
"""