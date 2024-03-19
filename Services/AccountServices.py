from flask import request


def register():
    username = request.form
    return {'username': username}
