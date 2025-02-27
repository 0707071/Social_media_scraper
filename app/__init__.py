from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "Hello@123"  # Set a secret key here
    app.config.from_object('config')

    from .routes import main
    app.register_blueprint(main)

    return app
