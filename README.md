# Career Agent - AI-Powered Professional Assistant

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Hugging%20Face-blue)](https://huggingface.co/spaces/Cavalgo/MyCareerAgent)
[![Python](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![OpenAI](https://img.shields.io/badge/Powered%20by-OpenAI%20GPT--4o-orange.svg)](https://openai.com)
[![Gradio](https://img.shields.io/badge/Interface-Gradio-red.svg)](https://gradio.app)

> **An intelligent conversational agent that represents my professional profile, answering questions about my experience, skills, and projects in real-time.**

## 🎯 Project Overview

This project demonstrates advanced AI integration skills by creating a personalized career assistant that acts as my digital professional representative. Built with modern Python frameworks and OpenAI's GPT-4, it showcases my ability to:

- **AI Integration**: Seamless OpenAI API implementation with function calling
- **Clean Architecture**: Well-structured, modular code design
- **Production Deployment**: Live application on Hugging Face Spaces
- **User Experience**: Intuitive chat interface with Gradio
- **Error Handling**: Robust error management and logging
- **Data Processing**: PDF parsing and text analysis capabilities

## 🛠️ Technical Stack

| Technology | Purpose | Implementation |
|------------|---------|----------------|
| **Python 3.8+** | Core language | Object-oriented design with type hints |
| **OpenAI GPT-4o** | Language model | Function calling, conversation management |
| **Gradio** | Web interface | Real-time chat interface |
| **PyPDF** | Document processing | Extract text from PDF profiles |
| **Pushover API** | Notifications | Real-time user interaction alerts |
| **Environment Variables** | Configuration | Secure API key management |

## 🚀 Key Features

### 🤖 Intelligent Conversation
- **Context-aware responses** based on my professional background
- **Natural language processing** for understanding complex queries
- **Personality simulation** that represents my professional persona

### 🔧 Advanced Tool Integration
- **Contact Recording**: Automatically captures interested user details
- **Question Logging**: Tracks unanswered queries for continuous improvement
- **Real-time Notifications**: Instant alerts for user interactions

### 📊 Smart Data Management
- **PDF Profile Parsing**: Extracts information from LinkedIn exports
- **Text Processing**: Handles multiple document formats
- **Error Recovery**: Graceful handling of missing files or API failures

## 🏗️ Architecture

```
career-agent/
├── app/
│   ├── main.py                 # Application entry point
│   ├── career_agent/
│   │   ├── __init__.py        # Package initialization
│   │   └── agent.py           # Core agent logic
│   └── me/
│       ├── profile.pdf        # LinkedIn profile data
│       └── summary.txt        # Professional summary
└── pyproject.toml             # Project dependencies
```

### Core Components

1. **Agent Engine** (`agent.py`):
   - OpenAI integration with function calling
   - Tool dispatch system for extensible functionality
   - Conversation state management

2. **Interface Layer** (`main.py`):
   - Gradio chat interface configuration
   - User interaction handling

3. **Data Layer** (`me/`):
   - Professional profile information
   - Structured summary data

## 💡 Technical Highlights

### OpenAI Function Calling Implementation
```python
TOOLS = [
    {"type": "function", "function": RECORD_USER_DETAILS_SCHEMA},
    {"type": "function", "function": RECORD_UNKNOWN_QUESTION_SCHEMA},
]

def handle_tool_calls(tool_calls):
    """Execute tool calls with proper error handling"""
    # Dynamic tool dispatch with error recovery
```

### Robust Error Handling
```python
def read_pdf_text(path: Path) -> str:
    """Extract text from PDF with graceful failure handling"""
    # Safe file operations with comprehensive logging
```

### Clean Architecture Pattern
- **Separation of concerns**: Clear boundaries between UI, business logic, and data
- **Dependency injection**: Configurable components for testing and deployment
- **Tool pattern**: Extensible function calling system

## 🎥 Live Demo

**Try it yourself**: [Career Agent on Hugging Face](https://huggingface.co/spaces/Cavalgo/MyCareerAgent)

Ask questions like:
- "What's your experience with Flutter development?"
- "Tell me about your recent projects"
- "What technologies do you work with?"
- "How can I contact you for opportunities?"

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key
- Optional: Pushover credentials for notifications

### Installation
```bash
# Clone the repository
git clone https://github.com/Cavalgo/career-agent.git
cd career-agent

# Navigate to app directory
cd app

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-openai-key"
export OPENAI_MODEL="gpt-4o-mini"

# Optional: Pushover notifications
export PUSHOVER_USER="your-pushover-user"
export PUSHOVER_TOKEN="your-pushover-token"

# Run the application
python main.py
```

### Deployment
```bash
# Deploy to Gradio (Hugging Face Spaces)
cd app
gradio deploy
```

## 📈 Impact & Results

- **🌐 Production Deployment**: Successfully deployed on Hugging Face Spaces
- **💬 Interactive Experience**: Provides 24/7 professional representation
- **📊 User Analytics**: Tracks engagement and common questions
- **🔄 Continuous Learning**: Logs unknown questions for profile improvements

## 🎯 Professional Skills Demonstrated

### **AI & Machine Learning**
- OpenAI GPT-4 integration and optimization
- Function calling and tool orchestration
- Conversational AI design patterns

### **Software Engineering**
- Clean code architecture and SOLID principles
- Error handling and logging best practices
- Configuration management and environment security

### **DevOps & Deployment**
- Cloud deployment on Hugging Face Spaces
- Environment configuration and secret management
- Production monitoring and logging

### **User Experience**
- Intuitive chat interface design
- Real-time interaction handling
- Responsive web application development

## 🔮 Future Enhancements

- [ ] **Multi-language Support**: Spanish/English conversation switching
- [ ] **Voice Integration**: Text-to-speech and speech-to-text capabilities
- [ ] **Analytics Dashboard**: User interaction insights and metrics
- [ ] **Integration APIs**: Webhook support for CRM systems
- [ ] **Mobile App**: React Native or Flutter mobile version

## 📞 Contact

**Carlos Antonio Vallejo González**
- 💼 **Role**: Flutter Mobile Developer & AI Integration Specialist
- 🌐 **Live Demo**: [Chat with my Career Agent](https://huggingface.co/spaces/Cavalgo/MyCareerAgent)
- 📧 **Email**: Available through the Career Agent
- 💻 **GitHub**: [@Cavalgo](https://github.com/Cavalgo)

---

*This project showcases my ability to integrate cutting-edge AI technologies with clean software engineering practices, creating production-ready applications that solve real-world problems.*