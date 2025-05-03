from flask import Blueprint, jsonify, request
from models.detalleVenta import DetalleVenta

detalleVenta= Blueprint('detalleVenta', __name__)
def get_detalle(id):
    detalle= DetalleVenta.query.get(id)#seguramente hay q corregir por id o algo, por ahora solo esta para marcar
    return jsonify(detalle.serialize())