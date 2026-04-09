# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

**Note**: This project is currently in the planning phase based on "校园问答智能体实施计划.md". The following guidance reflects the planned architecture and development workflow described in that document.

## Architecture Overview

This is a campus Q&A agent graduation project using RAG (Retrieval-Augmented Generation) technology. The system follows a frontend-backend separation architecture:

- **Frontend**: React 18 with TypeScript, using Vite for building. UI components from Ant Design or Material-UI. State management with React Context or Zustand.
- **Backend**: Python Flask with SQLAlchemy ORM. Database: SQLite (development) / MySQL (production). Vector storage: FAISS for local similarity search.
- **Knowledge Base System**: Web crawlers (Scrapy/BeautifulSoup), document processors, QA pair generators using domestic Chinese LLM APIs (iFlyTek Spark or Baidu Wenxin).
- **RAG Pipeline**: Text embedding → FAISS vector storage → retrieval → LLM API integration for answer generation.

### Planned Directory Structure
```
campus-qa-agent/
├── backend/           # Flask application
│   ├── app.py                    # Main Flask app
│   ├── requirements.txt          # Python dependencies
│   ├── config.py                 # Configuration
│   ├── database/                 # Database models and initialization
│   ├── knowledge/                # Crawlers, processors, QA generators, vector store
│   ├── rag/                      # Retrieval, generation, evaluation
│   └── api/                      # RESTful API routes
├── frontend/          # React TypeScript application
│   ├── package.json              # Node.js dependencies
│   ├── vite.config.ts            # Vite configuration
│   └── src/                      # Source code
├── data/              # Raw and processed data
│   ├── crawled/                  # Scraped website data
│   ├── processed/                # Cleaned documents
│   └── qa_pairs/                 # Generated question-answer pairs
└── docs/              # Project documentation
```

## Development Commands (Planned)

### Knowledge Base Construction
```bash
# Run crawler to collect data from campus websites
python backend/knowledge/crawler.py --site [URL]

# Process documents and extract text
python backend/knowledge/processor.py --input data/crawled --output data/processed

# Generate QA pairs using LLM API
python backend/knowledge/qa_generator.py --input data/processed --output data/qa_pairs

# Build FAISS vector index from QA pairs
python backend/knowledge/vector_store.py --qa data/qa_pairs --output indexes/faiss_index
```

### Backend Development
```bash
# Install Python dependencies
cd backend
pip install -r requirements.txt

# Run Flask development server
python app.py
# Server starts at http://localhost:5000

# Test the问答 API
curl -X POST http://localhost:5000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "图书馆开放时间是几点？"}'
```

### Frontend Development
```bash
# Install Node.js dependencies
cd frontend
npm install

# Start Vite development server
npm run dev
# App available at http://localhost:5173

# Build for production
npm run build
```

### Database Operations
```bash
# Initialize database (when models are defined)
python backend/database/init_db.py
```

## Key Integration Points

1. **LLM API Configuration**: Domestic Chinese APIs (iFlyTek Spark or Baidu Wenxin) require API keys stored in environment variables or config file.
2. **Vector Embeddings**: Use `sentence-transformers` for Chinese text embeddings; model files may need to be downloaded.
3. **Cross-Origin Requests**: Flask-CORS must be configured to allow frontend (localhost:5173) to access backend (localhost:5000).
4. **Data Storage**: FAISS indexes are binary files; keep them out of git. MySQL credentials should be in environment variables.

## Development Timeline (4-Week Plan)

1. **Week 1**: Project initialization, database design, crawler development
2. **Week 2**: RAG engine implementation, vector storage, LLM API integration
3. **Week 3**: Backend API and frontend interface development
4. **Week 4**: Testing, optimization, documentation

When implementing, prioritize the core RAG pipeline and basic chat interface for the graduation demonstration.