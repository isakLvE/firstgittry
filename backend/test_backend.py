#!/usr/bin/env python
"""
Quick test script to verify backend setup.
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_config():
    """Test configuration loading."""
    print("Testing configuration...")
    from config import Config, get_config

    config = Config()
    assert config.FLASK_ENV == 'development'
    assert config.SQLALCHEMY_DATABASE_URI is not None
    assert 'sqlite:///' in config.SQLALCHEMY_DATABASE_URI
    print("✓ Configuration loaded successfully")

def test_models():
    """Test database models."""
    print("\nTesting database models...")
    from database.models import Conversation, Message, Feedback, QAPair

    # Check model definitions
    assert Conversation.__tablename__ == 'conversations'
    assert Message.__tablename__ == 'messages'
    assert Feedback.__tablename__ == 'feedback'
    assert QAPair.__tablename__ == 'qa_pairs'

    # Check columns exist
    conv = Conversation()
    assert hasattr(conv, 'id')
    assert hasattr(conv, 'session_id')
    assert hasattr(conv, 'title')

    msg = Message()
    assert hasattr(msg, 'role')
    assert hasattr(msg, 'content')

    print("✓ Database models defined correctly")

def test_api_endpoints():
    """Test API endpoint imports."""
    print("\nTesting API endpoints...")

    # Mock flask app for testing
    from flask import Flask
    app = Flask(__name__)

    with app.app_context():
        # Import should work
        from api import api_bp
        from api.health import health_check
        from api.ask import ask_question

        # Check blueprint
        assert api_bp.name == 'api'
        assert api_bp.url_prefix == '/api'

        # Check routes are registered
        rules = [rule for rule in app.url_map.iter_rules()]
        # Note: Routes are registered when blueprint is registered with app

    print("✓ API endpoints imported successfully")

def test_app_factory():
    """Test Flask application factory."""
    print("\nTesting Flask application factory...")

    from app import create_app

    app = create_app('testing')

    # Check app configuration
    assert app.config['TESTING'] == True
    assert 'sqlite:///:memory:' in app.config['SQLALCHEMY_DATABASE_URI']

    # Check blueprints are registered
    blueprints = [bp.name for bp in app.blueprints.values()]
    assert 'api' in blueprints

    print("✓ Application factory works correctly")

def test_database_init():
    """Test database initialization script."""
    print("\nTesting database initialization...")

    # Test the script structure
    from database import init_db

    # Check functions exist
    assert hasattr(init_db, 'init_database')
    assert hasattr(init_db, 'check_database_connection')

    print("✓ Database initialization script structure valid")

def main():
    """Run all tests."""
    print("=" * 60)
    print("Backend Setup Verification")
    print("=" * 60)

    tests = [
        test_config,
        test_models,
        test_api_endpoints,
        test_app_factory,
        test_database_init
    ]

    passed = 0
    total = len(tests)

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} failed: {e}")

    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60)

    if passed == total:
        print("🎉 Backend setup verification successful!")
        return 0
    else:
        print("⚠️  Some tests failed. Check the implementation.")
        return 1

if __name__ == '__main__':
    sys.exit(main())