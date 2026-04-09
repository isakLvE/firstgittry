"""
Main Flask application for Campus Q&A Agent.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from config import get_config

# Initialize extensions
db = SQLAlchemy()

def create_app(config_name=None):
    """
    Application factory pattern for Flask.

    Args:
        config_name: Configuration name ('development', 'testing', 'production')
    """
    app = Flask(__name__)

    # Load configuration
    config = get_config(config_name)
    app.config.from_object(config)
    config.init_app(app)

    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG if app.config['DEBUG'] else logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Initialize extensions with app
    CORS(app, origins=app.config['CORS_ORIGINS'])
    db.init_app(app)

    # Import and register blueprints
    from api import api_bp
    app.register_blueprint(api_bp)

    # Create database tables
    with app.app_context():
        db.create_all()
        app.logger.info("Database tables created/verified")

    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': '校园问答智能体后端服务',
            'status': 'running',
            'version': '0.1.0',
            'endpoints': {
                'health': '/api/health',
                'status': '/api/status',
                'ask': '/api/ask',
                'ask_batch': '/api/ask/batch',
                'feedback': '/api/ask/feedback'
            }
        })

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal server error: {error}")
        return jsonify({'error': 'Internal server error'}), 500

    return app

# Create application instance
app = create_app(os.getenv('FLASK_CONFIG', 'development'))

if __name__ == '__main__':
    # Run development server
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'

    app.logger.info(f"Starting Campus Q&A Agent backend on port {port}")
    app.logger.info(f"Debug mode: {debug}")
    app.logger.info(f"Database: {app.config['SQLALCHEMY_DATABASE_URI']}")

    app.run(debug=debug, port=port, host='0.0.0.0')