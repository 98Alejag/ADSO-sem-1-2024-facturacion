from flask import render_template
from flask_controller import FlaskController 
from src.app import app   

class HomeController(FlaskController):
    @app.route('/')
    def index():
        return render_template('index.html', titulo='Bienvenido a la aplicación de facturación')