from os import getenv

from functools import wraps

from flask import request, abort
from node_agent.config import settings


# The actual decorator function
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        if request.headers.get('Grpc-Metadata-Authorization'):
            header = request.headers.get('Grpc-Metadata-Authorization')
            if header == 'Bearer ' + settings.NODE_AGENT_API_TOKEN:
                return view_function(*args, **kwargs)
            else:
                print('Error : invalid token')
                abort(401)
        else:
            print('Error : no token set')
            abort(401)
    return decorated_function
