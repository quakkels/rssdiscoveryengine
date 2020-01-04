from flask import Flask

def create_app():
	app = Flask(__name__)
	
	from . import home
	app.register_blueprint(home.bp)
	
	return app