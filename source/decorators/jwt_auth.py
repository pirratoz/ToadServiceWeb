def jwt_auth_required(handler):
    handler.__auth_required__ = True
    return handler
