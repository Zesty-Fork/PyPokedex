from flask import Flask
from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app: Flask = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.pokedex import bp as pokedex_bp
    app.register_blueprint(pokedex_bp, url_prefix="/pokedex")

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/test/")
    def test_page():
        return "<h1>Testing the Flask Application Factory Pattern</h1>"

    return app
