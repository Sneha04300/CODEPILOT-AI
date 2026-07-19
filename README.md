# CodePilot AI

### The Next Generation AI Engineering Workspace

CodePilot AI is an AI-powered software engineering platform designed to help developers understand, analyze, optimize, and maintain software repositories using Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), semantic code search, and intelligent code analysis.

Unlike traditional AI coding assistants that focus only on code generation, CodePilot AI understands the entire repository structure. It enables developers to explore large codebases, visualize software architecture, generate documentation, detect potential issues, and interact with their projects using natural language.

---

## Features

### Authentication
- Secure User Authentication
- JWT-based Authorization
- Protected Routes
- GitHub OAuth (Upcoming)

### Repository Management
- Upload Repository (ZIP)
- Connect GitHub Repository
- Repository Dashboard
- Repository Overview

### AI Workspace
- AI Code Chat
- Repository Question Answering
- Explain Functions and Classes
- Folder Structure Explanation
- Semantic Code Search

### Architecture Intelligence
- Automatic Architecture Visualization
- Dependency Graph Generation
- Component Relationship Mapping
- Mermaid Diagram Generation

### AI Bug Detection (Upcoming)
- Detect Potential Bugs
- Logic Error Analysis
- Performance Suggestions
- Code Smell Detection

### Security Scanner (Upcoming)
- OWASP Security Checks
- Secret Detection
- Dependency Vulnerability Analysis
- Security Recommendations

### Documentation Generator (Upcoming)
- README Generation
- API Documentation
- Inline Documentation
- Project Summary

### Developer Analytics (Upcoming)
- Repository Statistics
- Technical Debt Analysis
- Code Complexity Metrics
- Developer Productivity Dashboard

### AI Interview Mode (Upcoming)
- Repository-based Interview Questions
- System Design Practice
- Code Explanation Practice
- Personalized Feedback

---

## Tech Stack

### Frontend
- React.js
- JavaScript
- Vite
- Tailwind CSS
- React Router
- Framer Motion
- Axios

### Backend
- FastAPI
- Python
- SQLAlchemy
- Pydantic
- JWT Authentication

### Database
- PostgreSQL
- Qdrant (Vector Database)
- Redis (Upcoming)

### Artificial Intelligence
- Google Gemini API
- LangGraph
- Sentence Transformers
- Tree-sitter
- Hugging Face Transformers
- Scikit-learn

### Deployment
- Docker
- Vercel
- Render
- GitHub Actions

---

## System Architecture

```text
                 React Frontend
                        │
                        ▼
                FastAPI Backend
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
  PostgreSQL Database             Qdrant Vector DB
        │                               │
        └───────────────┬───────────────┘
                        ▼
                  LangGraph Workflow
                        │
                        ▼
                  Google Gemini API
                        │
                        ▼
                  AI Generated Results
```

---

## Project Structure

```text
codepilot-ai/

├── frontend/
├── backend/
├── docs/
├── assets/
├── README.md
├── LICENSE
└── .gitignore
```

---

## Development Roadmap

### Phase 1
- Authentication
- Dashboard
- Repository Upload
- Repository Management

### Phase 2
- Repository Parsing
- Tree-sitter Integration
- Embedding Generation
- Qdrant Integration
- AI Code Chat

### Phase 3
- Architecture Generator
- Semantic Code Search
- Documentation Generator
- Security Scanner

### Phase 4
- AI Bug Detection
- Technical Debt Analyzer
- AI Interview Mode
- Developer Analytics
- Multi-Agent AI

---

## Objectives

- Build an AI-powered engineering workspace for developers.
- Improve software understanding through intelligent repository analysis.
- Automate repetitive engineering tasks using AI.
- Simplify onboarding for large codebases.
- Demonstrate modern AI Engineering concepts including LLMs, RAG, Vector Databases, Static Code Analysis, and Intelligent Code Retrieval.

---

## Current Status

Project is currently under active development.

Completed:
- Project Initialization
- Repository Setup
- Frontend Setup

In Progress:
- Authentication Module

Upcoming:
- Dashboard
- Repository Management
- AI Workspace

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/Sneha04300/codepilot-ai.git
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## Future Enhancements

- Multi-Agent AI System
- GitHub Pull Request Review
- AI Code Review
- Security Vulnerability Scanner
- Technical Debt Prediction
- VS Code Extension
- Team Collaboration
- Cloud Deployment
- Enterprise Features

---

## License

This project is licensed under the MIT License.

---

## Author

Sneha Gupta

2ND YEAR Computer Science Engineering Student-BML MUNJAL UNIVERSITY 

GitHub: https://github.com/Sneha04300