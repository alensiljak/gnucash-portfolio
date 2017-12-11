"""
Decorators for Flask.
This is a test for custom decorators.
Templated is not used, however, as it is not compatible with setting up template location in flask.
"""
from functools import wraps
from flask import request, render_template

def templated(template=None):
    """
    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/#templating-decorator
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator