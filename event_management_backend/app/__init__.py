import os
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from dotenv import load_dotenv

from .models import db
from .routes.health import blp as health_blp

# Import blueprints
from .routes.events import blp as events_blp
from .routes.attendees import blp as attendees_blp
from .routes.tickets import blp as tickets_blp
from .routes.schedules import blp as schedules_blp

# Load environment vars (if .env present)
load_dotenv()

app = Flask(__name__)
app.url_map.strict_slashes = False

# CORS config based on env var or allow frontend default
frontend_origin = os.getenv("CORS_ORIGINS", "http://localhost:3000")
CORS(app, resources={r"/*": {"origins": frontend_origin}})

app.config["API_TITLE"] = "Event Management API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-secret")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///:memory:")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

api = Api(app)
api.register_blueprint(health_blp)
api.register_blueprint(events_blp)
api.register_blueprint(attendees_blp)
api.register_blueprint(tickets_blp)
api.register_blueprint(schedules_blp)

# Basic schema creation on first run (only if not using migrations)
with app.app_context():
    db.create_all()
