from flask import Blueprint, jsonify, request
from models.telefono import Telefono

telefono= Blueprint('telefono',__name__)
def get_telefonos():
    telefonos_clientes=Telefono.query.all()
    return jsonify ([telefono.serialize() for telefono in telefonos_clientes])