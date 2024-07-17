from flask import Flask


from config import Config
from app.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.debug = True
    

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.tags import bp as tags_bp
    app.register_blueprint(tags_bp)

    from app.specialists import bp as specialists_bp
    app.register_blueprint(specialists_bp)

    from app.users import bp as users_bp
    app.register_blueprint(users_bp)

    from app.requests import bp as requests_bp
    app.register_blueprint(requests_bp)

    from app.manychat import bp as manychat_bp
    app.register_blueprint(manychat_bp)

    from app.telegram import bp as telegram_bp
    app.register_blueprint(telegram_bp)

    from app.feedbacks import bp as feedbacks_bp
    app.register_blueprint(feedbacks_bp)

    db.create_all()

    return app  