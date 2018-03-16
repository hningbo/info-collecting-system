from flask import Flask, render_template, request
from werkzeug.utils import find_modules, import_string


def create_app(config=None):
    app = Flask('info-sys')
    app.config.update(dict(
        DEBUG=True,
        USERNAME='admin',
        PASSWORD='default',
        ))
    register_blueprints(app)
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(host='localhost', port=5000)


def register_blueprints(app):
    """Register all blueprint modules

    register blueprint
    
    """
    for name in find_modules('blueprints'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)
    return None


def main():
    create_app()


if __name__ == '__main__':
    main()
