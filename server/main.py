from app.routes import bp as api_bp
from flask_cors import CORS
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(api_bp)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
