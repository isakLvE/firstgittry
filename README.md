# 校园问答智能体 (Campus Q&A Agent)

基于RAG技术的校园问答系统毕业项目，提供智能化的校园信息查询服务。

## 📚 目录

- [项目简介](#项目简介)
- [项目结构](#项目结构)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [开发计划](#开发计划)
- [API接口](#api接口)
- [部署指南](#部署指南)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 🎯 项目简介

本项目是一个基于RAG (Retrieval-Augmented Generation) 技术的校园问答智能体，旨在为师生提供准确、及时的校园信息查询服务。系统通过爬取校园网站数据，构建知识库，利用向量检索和国内LLM API生成回答。

### 主要特性
- 🔍 **智能检索**：结合关键词匹配和向量相似度检索
- 🤖 **中文优化**：针对中文文本处理的RAG管道
- 🏫 **校园场景**：专注于校园常见问题解答
- 🚀 **前后端分离**：React前端 + Python后端现代化架构
- 📊 **可扩展性**：模块化设计，便于功能扩展

## 📁 项目结构

```
campus-qa-agent/
├── backend/                 # Flask/FastAPI 后端应用
│   ├── app.py              # 主应用文件
│   ├── requirements.txt    # Python依赖
│   ├── config.py          # 配置文件
│   ├── database/          # 数据库模型和初始化
│   ├── knowledge/         # 爬虫、处理器、QA生成器、向量存储
│   ├── rag/              # 检索、生成、评估模块
│   └── api/              # RESTful API路由
├── frontend/              # React TypeScript 前端应用
│   ├── package.json       # Node.js依赖
│   ├── vite.config.ts    # Vite配置
│   └── src/              # 源代码目录
├── data/                  # 数据目录
│   ├── crawled/          # 爬取的原始数据
│   ├── processed/        # 处理后的文档
│   └── qa_pairs/         # 生成的问答对
└── docs/                 # 项目文档
    ├── technical_design.md
    ├── api_documentation.md
    └── deployment_guide.md
```

## 🛠️ 技术栈

### 后端技术
- **框架**：FastAPI (推荐) 或 Flask
- **数据库**：SQLite (开发) / MySQL (生产)
- **ORM**：SQLAlchemy
- **向量存储**：FAISS / ChromaDB
- **中文嵌入模型**：sentence-transformers (text2vec-base-chinese)
- **LLM API**：科大讯飞星火 / 百度文心
- **爬虫框架**：Scrapy / BeautifulSoup

### 前端技术
- **框架**：React 18 + TypeScript
- **构建工具**：Vite
- **UI组件库**：Ant Design / Material-UI
- **状态管理**：React Context / Zustand
- **HTTP客户端**：Axios

### 开发运维
- **版本控制**：Git
- **容器化**：Docker + Docker Compose
- **CI/CD**：GitHub Actions
- **代码质量**：ESLint, Prettier, Black, Flake8

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 5.7+ (生产环境)

### 后端设置
```bash
# 克隆仓库
git clone <repository-url>
cd campus-qa-agent/backend

# 安装Python依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑.env文件，设置API密钥和数据库连接

# 初始化数据库
python database/init_db.py

# 启动开发服务器
python app.py
# 服务运行在 http://localhost:5000
```

### 前端设置
```bash
cd ../frontend

# 安装Node.js依赖
npm install

# 启动开发服务器
npm run dev
# 应用运行在 http://localhost:5173
```

### 知识库构建
```bash
# 运行爬虫收集数据
python backend/knowledge/crawler.py --site <校园网站URL>

# 处理文档
python backend/knowledge/processor.py --input data/crawled --output data/processed

# 生成QA对
python backend/knowledge/qa_generator.py --input data/processed --output data/qa_pairs

# 构建向量索引
python backend/knowledge/vector_store.py --qa data/qa_pairs --output indexes/faiss_index
```

## 📅 开发计划 (4周)

### 第1周：项目初始化
- [ ] 项目架构设计和技术选型确认
- [ ] 数据库设计并初始化
- [ ] 校园网站爬虫开发
- [ ] 基础开发环境搭建

### 第2周：RAG引擎实现
- [ ] 文本处理和数据清洗模块
- [ ] 向量存储和检索系统
- [ ] LLM API集成和提示工程
- [ ] 核心RAG管道测试

### 第3周：前后端开发
- [ ] 后端RESTful API实现
- [ ] 前端聊天界面开发
- [ ] 前后端联调和集成测试
- [ ] 基础功能验证

### 第4周：测试与优化
- [ ] 系统测试和bug修复
- [ ] 性能优化和压力测试
- [ ] 文档编写和代码整理
- [ ] 部署准备和演示准备

## 🔌 API接口

### 问答接口
```http
POST /api/ask
Content-Type: application/json

{
  "question": "图书馆开放时间是几点？",
  "user_id": "optional_user_id"
}
```

响应示例：
```json
{
  "answer": "图书馆的开放时间是周一至周五 8:00-22:00，周末 9:00-21:00。",
  "sources": [
    {
      "title": "图书馆官方网站",
      "url": "https://library.campus.edu.cn/hours",
      "confidence": 0.92
    }
  ],
  "confidence": 0.88,
  "response_time": 1.2
}
```

### 其他接口
- `GET /api/health` - 服务健康检查
- `POST /api/feedback` - 答案反馈收集
- `GET /api/history` - 用户查询历史
- `POST /api/train` - 模型训练接口（管理员）

## 🚢 部署指南

### Docker部署
```bash
# 构建和运行所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### 生产环境建议
1. **服务器配置**：至少2核4GB内存
2. **数据库**：使用MySQL生产数据库
3. **反向代理**：Nginx配置SSL和负载均衡
4. **监控**：配置基础监控和日志收集
5. **备份**：定期备份数据和向量索引

### 环境变量配置
```bash
# 必需配置
LLM_API_KEY=your_api_key
LLM_API_TYPE=iflytek  # iflytek 或 baidu
DATABASE_URL=mysql://user:password@localhost/campus_qa
SECRET_KEY=your_secret_key

# 可选配置
CACHE_REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
MAX_CONTENT_LENGTH=16777216
```

## 👥 贡献指南

### 开发流程
1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### 代码规范
- Python代码遵循PEP 8规范
- TypeScript代码使用严格的类型检查
- 提交信息遵循Conventional Commits规范
- 新功能必须包含测试用例

### 测试要求
```bash
# 运行Python测试
cd backend
pytest

# 运行前端测试
cd frontend
npm test

# 运行端到端测试
npm run test:e2e
```

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 项目Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 电子邮件: your-email@example.com

---

**感谢使用校园问答智能体！** 🎓
