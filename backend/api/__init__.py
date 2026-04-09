"""
API Blueprint for Campus Q&A Agent.
Register all API endpoints here.
"""
from flask import Blueprint

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Import routes to register them with the blueprint
from . import health, ask