from flask import Flask
from .scheduler import start_scheduler

def create_app():
  app = Flask(__name__) 
  #app.register_blueprint(main, url_prefix='/api')
  app.config.from_pyfile('../instance/config.py',silent=True)

  from .routes import main
  app.register_blueprint(main)
  start_scheduler()
  return app