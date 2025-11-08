# 🛠️ OpenCode Tools & Plugins Inventory

*Comprehensive list of all available tools, plugins, and extensions*

---

## 🤖 **AGENTS** (3)

| Agent | Purpose | Command | Status |
|-------|---------|---------|--------|
| **Code Reviewer** | Static code analysis and quality checks | `python cli.py review <file>` | ✅ Active |
| **Tester** | Automated test discovery and execution | `python cli.py test` | ✅ Active |
| **Deployer** | Automated deployment pipeline | `python cli.py deploy [branch]` | ✅ Active |

---

## 🛠️ **TOOLS** (7)

| Tool | Purpose | Features | Command |
|------|---------|----------|---------|
| **Hierarchical Memory** | Advanced SQLite-based memory management | Hierarchical nodes, semantic relationships, tag search | `python cli.py hierarchical_memory <action>` |
| **Memory Manager** | Basic conversation memory storage | Session-based storage, SQLite persistence | `python cli.py memory <action>` |
| **Code Analyzer** | Comprehensive code metrics and analysis | Multi-language support, complexity metrics | `python cli.py analyze_code <action>` |
| **OpenAPI Validator** | OpenAPI specification validation | Schema validation, structure verification | `python cli.py validate_openapi <spec>` |
| **Project Manager** | Project template creation and management | Multi-language templates, scaffolding | `python cli.py create_project <action>` |
| **Data Fetcher** | HTTP data retrieval and API interaction | JSON API handling, custom headers | `python cli.py fetch_data <url>` |
| **Format Converter** | JSON formatting and conversion | Pretty-print formatting, file conversion | `python cli.py convert_format <input> <output>` |

---

## 🌐 **MCP SERVERS** (23+)

### **Local MCP Servers** (3 - ✅ Active)

| Server | Access | Commands | Status |
|--------|--------|----------|--------|
| **Filesystem Server** | Local directories | `list_files`, `read_file` | ✅ Working |
| **Memory Server** | Hierarchical memory | `create_session`, `add_conversation`, `search_by_tag` | ✅ Working |
| **Git Server** | Git operations | `status`, `log`, `branches` | ✅ Working |

### **Cloud MCP Servers** (20+ - 🚀 Ready)

| Category | Servers | Installation |
|----------|---------|--------------|
| **Core** | memory, fetch, filesystem | `npm install @modelcontextprotocol/server-*` |
| **Development** | github, git, python | `npm install @modelcontextprotocol/server-*` |
| **Database** | sqlite, postgres | `npm install @modelcontextprotocol/server-*` |
| **Web** | puppeteer, brave-search, tavily | `npm install @modelcontextprotocol/server-*` |
| **Infrastructure** | docker, kubernetes, aws | `npm install @modelcontextprotocol/server-*` |
| **Integrations** | slack, gdrive, context7 | `npm install @modelcontextprotocol/server-*` |

---

## 📦 **EXTENSIONS** (6 Downloaded)

| Extension | Language | Purpose | Status |
|-----------|----------|---------|--------|
| **OpenCode MCP Tool** | TypeScript | Direct OpenCode CLI integration | ✅ Ready |
| **AI Sessions MCP** | Go | Cross-AI session search | ✅ Ready |
| **LLMs** | Python | Centralized LLM configuration | ✅ Ready |
| **System Prompt Orchestrator** | Python | Multi-agent workflow coordination | ✅ Ready |
| **FastMCP** | Python | Rapid MCP server development | ✅ Ready |
| **MCP-Box** | TypeScript | Universal MCP management | ✅ Ready |

---

## 🔗 **INTEGRATIONS** (3)

| Integration | Services | Features |
|-------------|----------|----------|
| **Automation** | GitHub | Issue creation/editing, token management |
| **Webhook Handler** | GitHub, GitLab, Linear | Multi-platform webhook processing |
| **Linear Manager** | Linear | Project management, issue tracking |

---

## ⚙️ **CONFIGS** (3)

| Config | Purpose | Features |
|--------|---------|----------|
| **FOSS Token Manager** | Secure token storage | Fernet encryption, local storage |
| **Memory Config** | Memory system settings | Database configuration, retention |
| **Token Manager** | Legacy token management | Basic token storage |

---

## 🎯 **QUICK COMMANDS**

### **Core Operations**
```bash
# Code Review
python cli.py review path/to/file.py

# Run Tests
python cli.py test

# Deploy Code
python cli.py deploy main

# Validate OpenAPI
python cli.py validate_openapi api.yaml
```

### **Memory Operations**
```bash
# Create Memory Session
python cli.py hierarchical_memory create_session "Project Planning"

# Add Conversation
python cli.py hierarchical_memory add_conversation <session_id> user "message"

# Search Memory
python cli.py hierarchical_memory search_tag "python"
```

### **MCP Server Management**
```bash
# Test Local Servers
python3 local_mcp_servers.py test

# List All Servers
python3 mcp_manager.py list

# Install Cloud Servers
python3 mcp_manager.py install github docker puppeteer
```

### **Token Management**
```bash
# Store Token
python cli.py foss_token store github "ghp_xxx"

# List Tokens
python cli.py foss_token list

# Export Tokens
python cli.py foss_token export backup.json
```

---

## 📊 **SUMMARY**

| Category | Count | Status |
|----------|-------|--------|
| **Agents** | 3 | ✅ All Active |
| **Tools** | 7 | ✅ All Active |
| **Local MCP Servers** | 3 | ✅ All Active |
| **Cloud MCP Servers** | 20+ | 🚀 Ready to Install |
| **Extensions** | 6 | ✅ Downloaded & Ready |
| **Integrations** | 3 | ✅ Configured |
| **Configs** | 3 | ✅ Active |

**🎉 Total: 42+ Active Components**

---

## 🚀 **NEXT STEPS**

1. **Install npm/uvx** for cloud MCP servers
2. **Test TUI application** (this tool!)
3. **Explore extension capabilities**
4. **Begin advanced implementations**

---

*Generated by OpenCode Tools TUI*