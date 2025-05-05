from flask import Blueprint, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from models.db import db
from models.categoria import Categoria

categoria_bp = Blueprint('categoria', __name__)

# Metodo get 
@categoria_bp.route('/api/categorias', methods=['GET'])
def get_categorias():
    categorias = Categoria.query.all()
    return jsonify([cat.serialize() for cat in categorias]), 200

# Metodo post
@categoria_bp.route('/api/categorias', methods=['POST'])
def create_categoria():
    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')

    if not nombre or not descripcion:
        return jsonify({'error': 'Faltan datos: nombre y/o descripción'}), 400

    nueva_categoria = Categoria(nombre=nombre, descripcion=descripcion)

    try:
        db.session.add(nueva_categoria)
        db.session.commit()
        return jsonify(nueva_categoria.serialize()), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# Metodo put remplazando  categorias
@categoria_bp.route('/api/categorias/<int:id>', methods=['PUT'])
def update_categoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({'error': 'Categoría no encontrada'}), 404

    data = request.get_json()
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')

    if not nombre or not descripcion:
        return jsonify({'error': 'Faltan datos: nombre y/o descripción'}), 400

    categoria.nombre = nombre
    categoria.descripcion = descripcion

    try:
        db.session.commit()
        return jsonify(categoria.serialize()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo patch para actualziar una categoria 
@categoria_bp.route('/api/categorias/<int:id>', methods=['PATCH'])
def patch_categoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({'error': 'Categoría no encontrada'}), 404

    data = request.get_json()
    if 'nombre' in data:
        categoria.nombre = data['nombre']
    if 'descripcion' in data:
        categoria.descripcion = data['descripcion']

    try:
        db.session.commit()
        return jsonify(categoria.serialize()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Metodo delete para eliminar categorias
@categoria_bp.route('/api/categorias/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    categoria = Categoria.query.get(id)
    if not categoria:
        return jsonify({'error': 'Categoría no encontrada'}), 404

    try:
        db.session.delete(categoria)
        db.session.commit()
        return jsonify({'mensaje': 'Categoría eliminada con éxito', 'categoria': categoria.serialize()}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500