"""
Core question-answering API endpoint for Campus Q&A Agent.
"""
from flask import request, jsonify, current_app
from datetime import datetime
import uuid
import json

@api_bp.route('/ask', methods=['POST'])
def ask_question():
    """
    Main问答 endpoint that processes user questions and returns answers.

    Request JSON:
    {
        "question": "图书馆开放时间是几点？",
        "session_id": "optional-session-id",
        "conversation_id": "optional-conversation-id",
        "user_id": "optional-user-id"
    }

    Response JSON:
    {
        "answer": "图书馆开放时间：周一至周五 8:00-22:00...",
        "conversation_id": "conv-123",
        "message_id": "msg-456",
        "sources": [
            {"id": "doc1", "title": "图书馆管理规定", "relevance": 0.95}
        ],
        "confidence": 0.92,
        "processing_time_ms": 1200,
        "model_used": "Spark-3.0"
    }
    """
    start_time = datetime.utcnow()

    # Parse request
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request must be JSON'}), 400

    question = data.get('question', '').strip()
    if not question:
        return jsonify({'error': 'Question is required'}), 400

    session_id = data.get('session_id', str(uuid.uuid4()))
    conversation_id = data.get('conversation_id')
    user_id = data.get('user_id')

    # Log the request
    current_app.logger.info(f"Question received: {question[:100]}... (session: {session_id})")

    try:
        # TODO: Integrate with RAG pipeline
        # For now, return a mock response
        answer, sources, confidence = process_question_with_rag(question)

        # Generate response
        processing_time = (datetime.utcnow() - start_time).total_seconds() * 1000

        response = {
            'answer': answer,
            'conversation_id': conversation_id or f"conv-{uuid.uuid4().hex[:8]}",
            'message_id': f"msg-{uuid.uuid4().hex[:8]}",
            'sources': sources,
            'confidence': confidence,
            'processing_time_ms': round(processing_time, 2),
            'model_used': 'mock-llm',  # TODO: Use actual model
            'timestamp': datetime.utcnow().isoformat()
        }

        # TODO: Store in database
        # store_conversation(session_id, user_id, question, response)

        return jsonify(response)

    except Exception as e:
        current_app.logger.error(f"Error processing question: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

def process_question_with_rag(question):
    """
    Mock RAG pipeline for demonstration.
    TODO: Replace with actual RAG implementation.
    """
    # Simple keyword matching for demo
    question_lower = question.lower()

    # Mock knowledge base
    knowledge_base = {
        '图书馆': {
            'answer': '图书馆开放时间：周一至周五 8:00-22:00，周六周日 9:00-21:00。节假日开放时间请关注图书馆公告。',
            'sources': [{'id': 'lib001', 'title': '图书馆管理规定', 'relevance': 0.95}],
            'confidence': 0.95
        },
        '校园卡': {
            'answer': '校园卡办理流程：1. 携带学生证和身份证到学生服务中心；2. 填写申请表；3. 缴纳工本费；4. 现场拍照制卡。办理时间：工作日 9:00-17:00。',
            'sources': [{'id': 'admin001', 'title': '学生事务处指南', 'relevance': 0.92}],
            'confidence': 0.92
        },
        '宿舍': {
            'answer': '宿舍楼晚上23:00关门，早上6:00开门。晚归同学需登记并联系宿管老师。',
            'sources': [{'id': 'dorm001', 'title': '宿舍管理规定', 'relevance': 0.90}],
            'confidence': 0.90
        },
        '食堂': {
            'answer': '学校食堂支持校园卡、支付宝、微信支付三种支付方式。推荐使用校园卡享受学生优惠。',
            'sources': [{'id': 'cafe001', 'title': '后勤服务中心公告', 'relevance': 0.88}],
            'confidence': 0.88
        },
        '体育馆': {
            'answer': '体育馆预约方式：1. 登录校园体育系统网站；2. 选择场地和时间段；3. 使用校园卡支付；4. 凭预约码入场。提前24小时开放预约。',
            'sources': [{'id': 'sports001', 'title': '体育部通知', 'relevance': 0.85}],
            'confidence': 0.85
        }
    }

    # Find best match
    best_match = None
    best_keyword = None

    for keyword, data in knowledge_base.items():
        if keyword in question_lower:
            if not best_match or len(keyword) > len(best_keyword):
                best_match = data
                best_keyword = keyword

    if best_match:
        return best_match['answer'], best_match['sources'], best_match['confidence']

    # Default response for unknown questions
    return (
        '抱歉，我暂时无法回答这个问题。'
        '您可以尝试询问关于图书馆、校园卡、宿舍、食堂或体育馆的相关信息。',
        [{'id': 'default', 'title': '通用回复', 'relevance': 0.5}],
        0.5
    )

@api_bp.route('/ask/batch', methods=['POST'])
def ask_batch():
    """
    Batch processing endpoint for multiple questions.

    Request JSON:
    {
        "questions": ["问题1", "问题2", "问题3"],
        "session_id": "optional-session-id"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request must be JSON'}), 400

    questions = data.get('questions', [])
    if not isinstance(questions, list) or len(questions) == 0:
        return jsonify({'error': 'Questions must be a non-empty array'}), 400

    session_id = data.get('session_id', str(uuid.uuid4()))

    results = []
    for i, question in enumerate(questions):
        try:
            answer, sources, confidence = process_question_with_rag(question)
            results.append({
                'question': question,
                'answer': answer,
                'sources': sources,
                'confidence': confidence,
                'success': True
            })
        except Exception as e:
            results.append({
                'question': question,
                'error': str(e),
                'success': False
            })

    return jsonify({
        'session_id': session_id,
        'results': results,
        'total': len(results),
        'successful': sum(1 for r in results if r.get('success', False)),
        'timestamp': datetime.utcnow().isoformat()
    })

@api_bp.route('/ask/feedback', methods=['POST'])
def submit_feedback():
    """
    Submit feedback on an answer.

    Request JSON:
    {
        "message_id": "msg-123",
        "rating": 5,
        "helpful": true,
        "correct": true,
        "comments": "很有帮助！"
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request must be JSON'}), 400

    message_id = data.get('message_id')
    if not message_id:
        return jsonify({'error': 'message_id is required'}), 400

    rating = data.get('rating')
    if rating is not None and (rating < 1 or rating > 5):
        return jsonify({'error': 'rating must be between 1 and 5'}), 400

    # TODO: Store feedback in database
    # store_feedback(message_id, data)

    return jsonify({
        'message': 'Feedback submitted successfully',
        'message_id': message_id,
        'timestamp': datetime.utcnow().isoformat()
    })