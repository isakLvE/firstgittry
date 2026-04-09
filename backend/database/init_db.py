#!/usr/bin/env python
"""
Database initialization script for Campus Q&A Agent.
Creates database tables and populates with sample data for development.
"""
import os
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Conversation, Message, Feedback, QAPair, SystemMetrics
import json
from datetime import datetime, timedelta

def init_database(database_url=None, create_sample_data=True):
    """
    Initialize the database with tables and optional sample data.

    Args:
        database_url: SQLAlchemy database URL. If None, uses default from config.
        create_sample_data: Whether to create sample data for development.
    """
    if database_url is None:
        # Use default SQLite path
        from config import Config
        database_url = Config.SQLALCHEMY_DATABASE_URI

    print(f"Initializing database: {database_url}")

    # Create engine and tables
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)

    print("✓ Database tables created successfully")

    if create_sample_data:
        # Create a session for adding sample data
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            # Sample QA pairs (campus-related questions)
            sample_qa_pairs = [
                {
                    "question": "图书馆开放时间是几点？",
                    "answer": "图书馆开放时间：周一至周五 8:00-22:00，周六周日 9:00-21:00。节假日开放时间请关注图书馆公告。",
                    "source": "学校官网",
                    "category": "library",
                    "tags": "开放时间,图书馆"
                },
                {
                    "question": "如何办理校园卡？",
                    "answer": "校园卡办理流程：1. 携带学生证和身份证到学生服务中心；2. 填写申请表；3. 缴纳工本费；4. 现场拍照制卡。办理时间：工作日 9:00-17:00。",
                    "source": "学生事务处",
                    "category": "administration",
                    "tags": "校园卡,办理"
                },
                {
                    "question": "宿舍晚上几点关门？",
                    "answer": "宿舍楼晚上23:00关门，早上6:00开门。晚归同学需登记并联系宿管老师。",
                    "source": "宿舍管理规定",
                    "category": "dormitory",
                    "tags": "宿舍,门禁"
                },
                {
                    "question": "食堂可以用支付宝支付吗？",
                    "answer": "可以，学校食堂支持校园卡、支付宝、微信支付三种支付方式。推荐使用校园卡享受学生优惠。",
                    "source": "后勤服务中心",
                    "category": "cafeteria",
                    "tags": "食堂,支付"
                },
                {
                    "question": "体育馆怎么预约？",
                    "answer": "体育馆预约方式：1. 登录校园体育系统网站；2. 选择场地和时间段；3. 使用校园卡支付；4. 凭预约码入场。提前24小时开放预约。",
                    "source": "体育部",
                    "category": "sports",
                    "tags": "体育馆,预约"
                },
                {
                    "question": "校医院在哪里？",
                    "answer": "校医院位于学校东门附近，具体位置：校园东区3号楼。联系电话：021-12345678。急诊24小时开放。",
                    "source": "校医院官网",
                    "category": "health",
                    "tags": "校医院,位置"
                },
                {
                    "question": "怎么申请奖学金？",
                    "answer": "奖学金申请流程：1. 登录学生信息系统查看奖学金类型；2. 准备申请材料（成绩单、推荐信等）；3. 在申请期内提交；4. 等待评审结果。详情咨询学生资助中心。",
                    "source": "学生资助中心",
                    "category": "academic",
                    "tags": "奖学金,申请"
                },
                {
                    "question": "校园网怎么连接？",
                    "answer": "校园网连接步骤：1. 搜索WiFi网络" Campus-WiFi"；2. 使用学号作为用户名，身份证后6位作为初始密码；3. 首次登录需激活账号。问题请联系信息中心：021-87654321。",
                    "source": "信息中心",
                    "category": "it",
                    "tags": "校园网,WiFi"
                },
                {
                    "question": "图书馆可以借几本书？",
                    "answer": "本科生可借10本，研究生可借15本，教师可借20本。借期30天，可续借一次（15天）。逾期每天罚款0.1元/本。",
                    "source": "图书馆借阅规则",
                    "category": "library",
                    "tags": "借书,图书馆"
                },
                {
                    "question": "怎么打印成绩单？",
                    "answer": "成绩单打印：1. 登录教务系统；2. 选择"成绩查询"；3. 点击"打印成绩单"；4. 到教务处盖章生效。自助打印机位于教务处大厅。",
                    "source": "教务处",
                    "category": "academic",
                    "tags": "成绩单,打印"
                }
            ]

            # Add sample QA pairs
            for qa_data in sample_qa_pairs:
                qa_pair = QAPair(**qa_data)
                session.add(qa_pair)

            # Add a sample conversation
            conversation = Conversation(
                session_id="sample-session-123",
                title="图书馆相关问题",
                user_id=None
            )
            session.add(conversation)
            session.flush()  # Get the conversation ID

            # Add sample messages
            messages = [
                Message(
                    conversation_id=conversation.id,
                    role="user",
                    content="图书馆开放时间是几点？",
                    created_at=datetime.utcnow() - timedelta(hours=2)
                ),
                Message(
                    conversation_id=conversation.id,
                    role="assistant",
                    content="图书馆开放时间：周一至周五 8:00-22:00，周六周日 9:00-21:00。节假日开放时间请关注图书馆公告。",
                    source_documents='[{"id": "doc1", "title": "图书馆管理规定"}]',
                    confidence_score=0.95,
                    processing_time_ms=1200,
                    model_used="Spark-3.0",
                    created_at=datetime.utcnow() - timedelta(hours=1, minutes=55)
                )
            ]

            for msg in messages:
                session.add(msg)

            # Add sample feedback
            feedback = Feedback(
                message_id=messages[1].id,
                rating=5,
                helpful=True,
                correct=True,
                comments="回答准确，很有帮助！"
            )
            session.add(feedback)

            # Add sample system metrics
            metrics = [
                SystemMetrics(
                    metric_type="response_time",
                    value=1.2,
                    details='{"endpoint": "/api/ask", "count": 10}'
                ),
                SystemMetrics(
                    metric_type="cache_hit_rate",
                    value=0.65,
                    details='{"cache_type": "query_cache"}'
                )
            ]

            for metric in metrics:
                session.add(metric)

            session.commit()
            print("✓ Sample data added successfully")
            print(f"  - {len(sample_qa_pairs)} QA pairs")
            print(f"  - 1 conversation with 2 messages")
            print(f"  - 1 feedback record")
            print(f"  - 2 system metrics")

        except Exception as e:
            session.rollback()
            print(f"✗ Error adding sample data: {e}")
            raise
        finally:
            session.close()

    print("✓ Database initialization complete")
    return engine

def check_database_connection(database_url):
    """Test database connection."""
    try:
        engine = create_engine(database_url)
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Initialize Campus Q&A Agent database")
    parser.add_argument("--database-url", help="Database URL (overrides config default)")
    parser.add_argument("--no-sample-data", action="store_true", help="Skip creating sample data")
    parser.add_argument("--check-only", action="store_true", help="Only check database connection")

    args = parser.parse_args()

    if args.check_only:
        from config import Config
        db_url = args.database_url or Config.SQLALCHEMY_DATABASE_URI
        check_database_connection(db_url)
    else:
        init_database(
            database_url=args.database_url,
            create_sample_data=not args.no_sample_data
        )