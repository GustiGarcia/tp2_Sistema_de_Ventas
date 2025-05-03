from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from models.db import db
from models.provedor import Provedor

provedor= Blueprint('provedor',__name__)
def get_provedores():
    provedores=Provedor.query.all()
    return jsonify([provedores.serialize() for provedor in provedores])
    