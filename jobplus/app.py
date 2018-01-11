from flask import Flask, render_template
from jobplus.config import configs  # 传入configs字典
from jobplus.models import db

def create_app(config):
    """APP工厂
    """
    app = Flask(__name__)
    app.config.from_object(configs.get(config))
    register_blueprints(app)
    register_extensions(app)
    return app


def register_blueprints(app):
    from  .handlers import front
    app.register_blueprint(front)


def register_extensions(app):
    db.init_app(app)
