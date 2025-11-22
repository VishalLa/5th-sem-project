import os
from flask import Flask, render_template
from application.login import login_controller
from application.prediction_controller import prediction_controller
from application.database import db
from application.config import LocalDevelopmentConfig

def create_app():

    # initilize flask app
    app = Flask(__name__)

    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)

    app.register_blueprint(login_controller)
    app.register_blueprint(prediction_controller)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    
    @app.route('/home')
    def home():
        return render_template('home.html')

    app.run(host='0.0.0.0', port=5000)
