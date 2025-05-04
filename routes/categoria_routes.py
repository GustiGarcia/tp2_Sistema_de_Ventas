from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.categoria import Categoria

categoria=Blueprint('categoria', __name__)

@categoria.route('/api/categoria', methods=['GET']) #GET
def get_categoria():
    categorias = Categoria.query.all()
    return jsonify([categoria.serialize() for categoria in categorias])

@categoria.route('/api/categoria/<id>', methods=['GET'])# GET BY ID / busqueda por id
def get_categoria_id(id):
    one_categoria=Categoria.query.get(id)
    if not one_categoria:
        return jsonify({'error': 'Categoria no encontrado'}),404
    return jsonify(one_categoria.serialize())