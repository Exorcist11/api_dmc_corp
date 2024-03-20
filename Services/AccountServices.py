from flask import request, jsonify
from Models.Roles import Role


def register():

    return jsonify({
        'status': 'success'
    }), 200
