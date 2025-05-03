from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.categoria import Categoria

categoria=Blueprint('categoria', __name__)

@categoria.route('/api/categoria')
def get_categoria():
    categorias=Categoria.query.all()
    return jsonify(Categoria.serialize())