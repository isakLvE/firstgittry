"""
Health check and system status endpoints.
"""
from flask import jsonify
from datetime import datetime
import psutil
import os
from ..database.models import Conversation, Message
from sqlalchemy import func

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Basic health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'campus-qa-agent-backend',
        'version': '0.1.0'
    })

@api_bp.route('/status', methods=['GET'])
def system_status():
    """Detailed system status including metrics."""
    try:
        # Get database statistics
        from ..database.models import Base
        from sqlalchemy import create_engine
        from ..config import Config

        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

        # Check database connectivity
        with engine.connect() as conn:
            conn.execute("SELECT 1")
            db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'

    # Get system metrics
    memory = psutil.virtual_memory()
    cpu_percent = psutil.cpu_percent(interval=0.1)
    disk = psutil.disk_usage('/')

    # Try to get application-specific metrics
    try:
        from .. import db
        conversation_count = Conversation.query.count()
        message_count = Message.query.count()
    except:
        conversation_count = 0
        message_count = 0

    return jsonify({
        'status': 'operational',
        'timestamp': datetime.utcnow().isoformat(),
        'system': {
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_gb': round(memory.available / (1024**3), 2),
            'disk_percent': disk.percent,
            'disk_free_gb': round(disk.free / (1024**3), 2)
        },
        'database': {
            'status': db_status,
            'conversations': conversation_count,
            'messages': message_count
        },
        'application': {
            'environment': os.getenv('FLASK_ENV', 'development'),
            'debug_mode': os.getenv('FLASK_DEBUG', '0') == '1'
        }
    })

@api_bp.route('/metrics', methods=['GET'])
def application_metrics():
    """Application-specific metrics for monitoring."""
    try:
        from ..database.models import SystemMetrics
        from sqlalchemy import desc

        # Get latest metrics of each type
        metrics = {}
        for metric_type in ['response_time', 'cache_hit_rate', 'error_rate']:
            latest = SystemMetrics.query.filter_by(
                metric_type=metric_type
            ).order_by(desc(SystemMetrics.timestamp)).first()

            if latest:
                metrics[metric_type] = {
                    'value': latest.value,
                    'timestamp': latest.timestamp.isoformat()
                }

        return jsonify({
            'metrics': metrics,
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'error': f'Failed to retrieve metrics: {str(e)}',
            'metrics': {}
        }), 500