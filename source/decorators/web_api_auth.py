def web_api_key_required(handler):
    handler.__web_api_key_auth_required__ = True
    return handler
