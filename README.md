# OpenCode Extensions

A comprehensive ecosystem of tools, plugins, and extensions for OpenCode - the AI-powered development assistant.

## 🚀 Overview

This repository contains **50+ components** organized into 6 main categories:

- 🤖 **Agents** (4): Code Reviewer, Tester, Deployer, **Multi-Agent Coordinator**
- 🛠️ **Tools** (9): Memory management, Code analysis, **Vector Database**, **Agent Communication**
- 🌐 **MCP Servers** (23+): Local and cloud Model Context Protocol servers
- 📦 **Extensions** (6): Downloaded and configured extensions
- 🔗 **Integrations** (3): External service integrations
- ⚙️ **Configs** (3): Configuration and security tools

## ✨ NEW: Multi-Agent Democratic Problem Solving

**Cutting-edge multi-agent AI system** based on academic research in distributed decision-making:

- 🧠 **Vector Databases**: ChromaDB, Qdrant, Weaviate for semantic knowledge storage
- 💬 **Redis Communication**: Democratic coordination between autonomous agents
- 🗳️ **6 Problem-Solving Strategies**: Voting, Consensus, Auction, Swarm, Debate, Hierarchical
- 🤝 **5 Agent Roles**: Problem-Solver, Monitor, Note-Taker, Healer, Coordinator
- 📚 **Academic Foundation**: Based on 2024-2025 research in multi-agent systems

See [MULTIAGENT_GUIDE.md](MULTIAGENT_GUIDE.md) for complete documentation.

## 🎯 Key Features

### ✅ **100% FOSS Compliant**
- All tools use Free and Open Source Software
- Self-hosted alternatives to proprietary services
- Local-first approach with privacy focus

### 🧠 **Advanced Memory System**
- Hierarchical SQLite-based memory management
- Semantic relationships and auto-categorization
- Tag-based search and consolidation

### 🌐 **MCP Server Ecosystem**
- 3 local MCP servers (filesystem, memory, git)
- 20+ cloud MCP servers ready for installation
- Model Context Protocol for AI integrations

### 🖥️ **Terminal UI**
- Beautiful Bubbletea-based TUI for tool management
- Interactive navigation and command execution
- Search and discovery features

## 📁 Repository Structure

```
opencode_extensions/
├── agents/              # AI agents for code tasks
├── tools/               # Core utilities and tools
├── local_mcp_servers/   # Custom MCP server implementations
├── extensions/          # Downloaded extensions
├── integrations/        # External service integrations
├── configs/            # Configuration management
├── tools-tui/          # Terminal User Interface
├── cli.py              # Main CLI interface
└── *.md               # Documentation
```

## 🏃‍♂️ Quick Start

### Prerequisites
- Python 3.8+
- Go 1.21+ (for TUI)
- Node.js/npm (for some extensions)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd opencode_extensions
   ```

2. **Setup Python environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt  # If available
   ```

3. **Test the CLI**:
   ```bash
   python3 cli.py --help
   ```

4. **Launch the TUI**:
   ```bash
   cd tools-tui
   go run .
   ```

## 🎮 Usage

### CLI Commands

#### Traditional Commands
```bash
# Code review
python3 cli.py review path/to/file.py

# Run tests
python3 cli.py test

# Memory operations
python3 cli.py hierarchical_memory create_session "Project Planning"

# MCP server management
python3 local_mcp_servers.py test

# Token management
python3 cli.py foss_token store github "your_token"
```

#### NEW: Multi-Agent Commands
```bash
# Run full multi-agent demonstration
python3 demo_multiagent.py

# Vector database operations
python3 cli.py vector_db init chromadb
python3 cli.py vector_db ingest document.txt
python3 cli.py vector_db search "semantic query"
python3 cli.py vector_db stats

# Agent communication
python3 cli.py agent_comm register agent1 problem_solver
python3 cli.py agent_comm vote "Proposal" "yes,no,abstain"
python3 cli.py agent_comm status
python3 cli.py agent_comm health

# Multi-agent problem solving
python3 cli.py multiagent demo
python3 cli.py multiagent spawn 5
python3 cli.py multiagent solve "Optimize code" voting
python3 cli.py multiagent status
```

### TUI Navigation
- `↑/↓` - Navigate tools
- `←/→` - Switch categories  
- `Enter` - View details
- `x` - Execute command
- `/` - Search
- `?` - Help

## 📊 Components Summary

| Category | Count | Status |
|----------|-------|--------|
| **Agents** | 3 | ✅ Active |
| **Tools** | 7 | ✅ Active |
| **Local MCP Servers** | 3 | ✅ Active |
| **Cloud MCP Servers** | 20+ | 🚀 Ready to Install |
| **Extensions** | 6 | ✅ Downloaded & Ready |
| **Integrations** | 3 | ✅ Configured |
| **Configs** | 3 | ✅ Active |

## 🔧 Configuration

### Environment Variables
```bash
export OPENCODE_EXTENSIONS_PATH="/path/to/opencode_extensions"
export FOSS_TOKEN_STORAGE_PATH="$HOME/.foss_tokens"
```

### MCP Settings
Configuration files are located in:
- Local: `mcp_settings_local.json`
- Global: `~/.config/Development/.vscode-server/.../mcp_settings.json`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your tool/extension
4. Update documentation
5. Submit a pull request

### Adding New Tools
1. Add to appropriate directory (`agents/`, `tools/`, etc.)
2. Update `cli.py` with new command
3. Add to TUI inventory in `tools-tui/models.go`
4. Update documentation

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [OpenCode](https://opencode.ai) - AI-powered development assistant
- [Model Context Protocol](https://modelcontextprotocol.io) - MCP specification
- [Bubbletea](https://github.com/charmbracelet/bubbletea) - TUI framework

## 📞 Support

- 📖 Documentation: Check the `.md` files in this repository
- 🐛 Issues: Open an issue on the repository
- 💬 Discussions: Use repository discussions feature

---

*Built with ❤️ for the OpenCode community*