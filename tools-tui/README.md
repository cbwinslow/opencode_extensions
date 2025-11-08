# 🛠️ OpenCode Tools TUI

A beautiful terminal user interface for managing and exploring your OpenCode tools, plugins, and extensions built with Bubbletea.

## 🚀 Features

- **Interactive Navigation**: Browse through 42+ tools across 6 categories
- **Detailed Views**: View tool descriptions, features, and commands
- **Command Execution**: Run tools directly from the TUI
- **Search Functionality**: Find tools quickly with search mode
- **Beautiful UI**: Modern terminal interface with colors and styling
- **Keyboard Shortcuts**: Efficient navigation with vim-like keys

## 📋 Categories

- 🤖 **Agents** (3): Code Reviewer, Tester, Deployer
- 🛠️ **Tools** (7): Memory, Code Analyzer, Project Manager, etc.
- 🌐 **MCP Servers** (23+): Local and cloud servers
- 📦 **Extensions** (6): Downloaded and ready to use
- 🔗 **Integrations** (3): GitHub, Linear, Webhook handlers
- ⚙️ **Configs** (3): Token managers and configuration

## 🎮 Controls

### Navigation
- `↑/k` - Move up
- `↓/j` - Move down  
- `←/h` - Previous category
- `→/l` - Next category
- `tab` - Toggle category visibility

### Actions
- `enter/space` - Select tool / View details
- `x` - Execute tool command
- `/` - Search mode
- `esc/q` - Go back / Exit mode

### Help
- `?` - Toggle help menu
- `ctrl+c/Q` - Quit application

## 🏃‍♂️ Usage

### From the OpenCode extensions directory:

```bash
cd tools-tui
go run .
```

Or build and run:

```bash
cd tools-tui
go build .
./tools-tui
```

## 📱 Screenshots

The TUI provides:
- **Main View**: Category and tool listing
- **Detail View**: In-depth tool information
- **Command Output**: Real-time command execution results
- **Search Mode**: Quick tool discovery

## 🛠️ Installation

### Prerequisites
- Go 1.21 or higher
- OpenCode extensions directory structure

### Build from source
```bash
git clone <repository>
cd opencode_extensions/tools-tui
go mod tidy
go build .
```

## 🎨 Customization

The TUI is fully customizable:
- Colors and styling in `ui.go`
- Tool data in `models.go`
- Key bindings in `KeyMap`

## 📊 Tool Data

The TUI loads tools from the comprehensive inventory including:
- **42+ active components**
- **6 major categories** 
- **20+ cloud MCP servers** ready for installation
- **100% FOSS compliance**

## 🤝 Contributing

1. Add new tools to `LoadToolsFromInventory()` in `models.go`
2. Customize styling in `ui.go`
3. Add new key bindings to `KeyMap`
4. Test with `go run .`

## 📄 License

MIT License - see LICENSE file for details

---

*Built with ❤️ using Bubbletea by Charm*