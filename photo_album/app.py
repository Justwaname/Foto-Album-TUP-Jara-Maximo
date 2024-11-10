from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app_init import create_app, db

app = create_app()
app.config.from_object(Config)

migrate = Migrate(app, db)

from routes import main as main_blueprint
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
