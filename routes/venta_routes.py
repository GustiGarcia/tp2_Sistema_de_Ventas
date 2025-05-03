from flask import Blueprint, jsonify, request
from models.venta import Venta

ventas= Blueprint('ventas',__name__)
def get_ventas():
    ventas=Venta.query.all()
    return jsonify(venta.serialize() for venta in ventas)
    