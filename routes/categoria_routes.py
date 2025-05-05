from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.categoria import Categoria

categoria=Blueprint('categoria', __name__)

@categoria.route('/api/categoria', methods=['GET']) #GET
def get_categoria():
    categorias = Categoria.query.all()
    return jsonify([categoria.serialize() for categoria in categorias])

"""@categoria.route('/api/categoria/<id>', methods=['GET'])# GET BY ID / busqueda por id
def get_categoria_id(id):
    one_categoria=Categoria.query.get(id)
    if not one_categoria:
        return jsonify({'error': 'Categoria no encontrado'}),404
    return jsonify(one_categoria.serialize())""" #IMAGINO QUE NO HACE FALTA BUSCAR POR ID


@categoria.route('/api/categoria', methods=['POST']) #POST INDIVIDUAL
def create_client():
    data = request.get_json() #Tomar datos enviados en formato json
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    #VALIDACION QUE NO FALTEN DATOS
    if not nombre or not descripcion:
        return jsonify({'error': 'faltan datos'}),400
    
#Crear Cliente (instanciamos???)
    nuevaCategoria = Categoria(nombre=nombre,descripcion=descripcion)

    #agregamos a base de datos
    db.session.add(nuevaCategoria)
    db.session.commit() #confirma y escribre la base de datos

    return jsonify(nuevaCategoria.serialize()), 201



@categoria.route('/api/categoria/<id>', methods=['PUT'])#metodo PUT , se coloca el id en la direccion y se pasa el json
def updateCategoria(id):
    update = Categoria.query.get(id)
    if not update:
        return jsonify({'Error': 'no se encontro categoria'}),404
    nuevoNombre=request.json['nombre']
    nuevaDescripcion=request.json['descripcion']

    update.nombre=nuevoNombre
    update.descripcion=nuevaDescripcion

    db.session.commit()
    return jsonify (update.serialize())


@categoria.route('/api/categoria/<id>', methods=(['PATCH']))
def patch_categoria(id):
    patch = Categoria.query.get(id)
    if not patch:
        return jsonify({'error': 'no se encontro categoria'}),404
    
    data = request.json
    if 'nombre' in data:
        patch.nombre= data['nombre']
    if 'descripcion' in data:
        patch.descripcion = data['descripcion']
    
    db.session.commit()
    return jsonify(patch.serialize())


@categoria.route('/api/categoria/<id>', methods = ['DELETE']) #Funciona con cliente sin vehiculo, revisar para eliminar vehiculos tambien
def delete_categoria(id):
    delete = Categoria.query.get(id)
    if not delete:
        return jsonify({'error': 'categoria no encontrado/registrado'}),404
    db.session.delete(delete)
    db.session.commit()

    return jsonify(delete.serialize())