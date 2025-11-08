# OpenCode Extensions Guide

## 🚀 Downloaded Extensions Overview

We've successfully downloaded and configured **6 major extensions** to expand OpenCode's functionality:

### 📋 Extension Summary

| Extension | Type | Status | Key Features |
|-----------|-------|---------|--------------|
| **opencode-mcp-tool** | MCP Server | ✅ Downloaded | Multi-model support, Plan mode, Slash commands |
| **ai-sessions-mcp** | MCP Server | ✅ Downloaded | Session search, BM25 ranking, Multi-LLM |
| **llms** | Management System | ✅ Downloaded | Feature-Implementer v2, Scope Intelligence |
| **systemprompt-code-orchestrator** | Orchestrator | ✅ Downloaded | Task management, Git integration |
| **fastmcp** | Framework | ✅ Downloaded | Rapid MCP development |
| **mcp-box** | CLI Tool | ✅ Downloaded | Server discovery, Configuration |

---

## 🔧 Installation & Setup

### 1. OpenCode MCP Tool
**Purpose**: Direct MCP integration with OpenCode CLI

```bash
# Quick Setup (one-liner)
claude mcp add opencode -- npx -y opencode-mcp-tool -- --model google/gemini-2.5-pro

# Verify Installation
claude mcp list
# Type /mcp in Claude Code to verify
```

**Features**:
- 🤖 Multi-model support via OpenCode
- 📋 Plan mode for structured analysis
- 🔄 Model selection (primary + fallback)
- ⚡ Slash commands (/plan, /build, /help, /ping)
- 🧠 Brainstorming capabilities

### 2. AI Sessions MCP Server
**Purpose**: Search across AI coding sessions

```bash
# Quick Install
curl -fsSL https://aisessions.dev/install.sh | bash

# Manual Download
# Download from: https://github.com/yoavf/ai-sessions-mcp/releases

# Build from Source (requires Go 1.25+)
cd extensions/ai-sessions-mcp
go build -o bin/aisessions ./cmd/ai-sessions
```

**Features**:
- 🔍 Search Claude Code, Gemini CLI, OpenCode sessions
- 📊 BM25 ranking for relevance
- 📄 Contextual snippets
- 📖 Pagination for large sessions
- ☁️ Upload to aisessions.dev

### 3. LLMs Configuration System
**Purpose**: Centralized LLM management and tooling

```bash
cd extensions/llms

# Install dependencies
pip3 install -r requirements.txt

# Setup the system
python3 -m llms setup

# Fetch documentation
python3 -m llms fetch-docs
```

**Features**:
- 🏗️ Feature-Implementer v2 (14 specialized agents)
- 🎯 Scope Intelligence (Global/Project/Local)
- 📚 Documentation fetcher for multiple LLMs
- 🛠️ Skill/Command/Agent/Prompt builders
- 🔌 Plugin builder for distribution
- 🪝 Hook configuration with quality gates

### 4. SystemPrompt Code Orchestrator
**Purpose**: Multi-agent workflow orchestration

```bash
cd extensions/systemprompt-code-orchestrator

# Install dependencies
npm install

# Setup orchestrator
npm run setup
```

**Features**:
- 🎭 Task management and process execution
- 🔄 Git integration
- 🤝 Multi-agent coordination
- ⚙️ Workflow automation
- 💻 Code generation and review

### 5. FastMCP Framework
**Purpose**: Rapid MCP server development

```bash
# Install FastMCP
pip3 install fastmcp

# Create a new MCP server
fastmcp create my-server

# Develop with Python framework
cd my-server
fastmcp dev
```

**Features**:
- ⚡ Rapid MCP server development
- 🐍 Python-based framework
- 📝 Simplified API
- 📋 Template generation
- 🧪 Testing utilities

### 6. MCP-Box Management Tool
**Purpose**: Universal MCP server management

```bash
# Install MCP-Box
npm install mcp-box

# Initialize MCP environment
mcp-box init

# Install servers
mcp-box install github
mcp-box install filesystem

# List installed servers
mcp-box list

# Configure servers
mcp-box configure github
```

**Features**:
- 🔍 Server discovery and installation
- ⚙️ Configuration management
- 📋 Registry integration
- 🔒 Security validation
- 🖥️ Multi-platform support

---

## 🎯 Use Cases & Workflows

### 📚 Research & Learning Workflow
```bash
# 1. Search previous sessions for similar problems
ai-sessions search "database connection issues"

# 2. Use OpenCode with multiple models for analysis
claude mcp ask opencode "Compare database connection patterns" --model gemini-2.5-pro

# 3. Create structured plan
/plan create database-migration-plan
```

### 🏗️ Development Workflow
```bash
# 1. Initialize project with LLMs system
llms project init my-app

# 2. Create development agents
llms agent create backend-developer --skills "python,fastapi,database"
llms agent create frontend-developer --skills "react,typescript,ui"

# 3. Orchestrate development
systemprompt run --agents backend-developer,frontend-developer --task "implement user auth"
```

### 🔌 Custom MCP Development
```bash
# 1. Create new MCP server with FastMCP
fastmcp create my-custom-tool

# 2. Develop tools
cd my-custom-tool
# Edit src/tools/

# 3. Test locally
fastmcp dev

# 4. Install with MCP-Box
mcp-box install ./my-custom-tool
```

---

## 🔄 Integration with Existing OpenCode Features

### Memory System Integration
```bash
# Store session findings in hierarchical memory
python3 cli.py hierarchical_memory create_session "Database Research"
python3 cli.py hierarchical_memory add_conversation <session_id> user "Found connection pooling issue"
python3 cli.py hierarchical_memory create_concept "Connection Pooling" "Database connection management technique"
```

### FOSS Token Management
```bash
# Store tokens for all services
python3 cli.py foss_token store github "your-github-token"
python3 cli.py foss_token store aisessions "your-session-token"
python3 cli.py foss_token store mattermost "your-mattermost-token"
```

### Code Analysis Integration
```bash
# Analyze extension code
python3 cli.py analyze_code analyze_directory extensions/

# Find duplicate code patterns
python3 cli.py analyze_code find_duplicates extensions/
```

---

## 📊 Performance & Security

### 🔒 Security Best Practices
- ✅ All extensions are open source
- ✅ Local token encryption with Fernet
- ✅ Self-hosted options available
- ✅ No proprietary dependencies
- ✅ Community-vetted code

### ⚡ Performance Optimization
- 🚀 Parallel session search with BM25
- 💾 Local caching for documentation
- 🔄 Lazy loading for MCP servers
- 📊 Resource monitoring with hooks

---

## 🛠️ Troubleshooting

### Common Issues

#### MCP Server Not Found
```bash
# Check MCP configuration
claude mcp list

# Reinstall server
claude mcp remove opencode
claude mcp add opencode -- npx -y opencode-mcp-tool
```

#### AI Sessions Not Loading
```bash
# Check session directory
ls -la ~/.aisessions/

# Rebuild from source
cd extensions/ai-sessions-mcp
go clean && go build -o bin/aisessions ./cmd/ai-sessions
```

#### LLMs System Dependencies
```bash
# Install Python dependencies
pip3 install -r extensions/llms/requirements.txt

# Check Python version
python3 --version  # Should be 3.11+
```

### Getting Help
- 📖 **Documentation**: Check each extension's `README.md`
- 🐛 **Issues**: Report on respective GitHub repositories
- 💬 **Community**: Join Discord/Slack communities
- 🔍 **Debugging**: Use `--verbose` flags for detailed logs

---

## 🚀 Advanced Usage

### Custom Agent Development
```python
# Create custom agent with LLMs system
from llms import AgentBuilder

agent = AgentBuilder("custom-analyzer") \
    .with_skills("code-analysis", "security-review") \
    .with_model("claude-3.5-sonnet") \
    .with_hooks("pre-commit", "post-review") \
    .build()
```

### Multi-Model Orchestration
```bash
# Use different models for different tasks
claude mcp ask opencode "Generate code" --model codellama
claude mcp ask opencode "Review security" --model claude-3.5-sonnet
claude mcp ask opencode "Plan architecture" --model gemini-2.5-pro
```

### Session Analytics
```bash
# Analyze coding patterns
ai-sessions analyze --pattern "bug-fixes" --timeline "last-30-days"

# Export session data
ai-sessions export --format json --output sessions.json
```

---

## 📈 Future Roadmap

### Upcoming Features
- 🔮 **Universal Agent Protocol**: Cross-platform agent communication
- 🌐 **Federated Learning**: Share improvements across instances
- 🧠 **Advanced Memory Integration**: Deeper hierarchical memory
- 🔌 **Plugin Marketplace**: Community-driven extension sharing
- 📊 **Analytics Dashboard**: Usage patterns and optimization

### Contributing
- 🤝 **Contributions Welcome**: All extensions accept PRs
- 📋 **Issue Templates**: Standardized bug reports
- 🧪 **Testing Framework**: Automated testing for all extensions
- 📚 **Documentation**: Help improve guides and examples

---

## 🎉 Summary

With these **6 powerful extensions**, your OpenCode setup now includes:

- **🤖 Multi-Model AI Support**: Access to Claude, Gemini, Llama, and more
- **🔍 Smart Session Search**: Find solutions across all AI coding sessions  
- **🏗️ Agent Orchestration**: Coordinate multiple specialized agents
- **🔌 Rapid MCP Development**: Build custom tools quickly
- **⚙️ Centralized Management**: Unified configuration and control
- **🧠 Enhanced Memory**: Hierarchical knowledge organization

All while maintaining **100% FOSS compliance** and **data sovereignty**! 🌟