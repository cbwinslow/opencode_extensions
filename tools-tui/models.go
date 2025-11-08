package main

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"strings"
)

// Tool represents a tool or plugin in the system
type Tool struct {
	Name        string
	Purpose     string
	Command     string
	Status      string
	Category    string
	Description string
	Features    []string
}

// Category represents a category of tools
type Category struct {
	Name    string
	Purpose string
	Tools   []Tool
	Active  bool
}

// LoadToolsFromInventory loads tools from the markdown inventory file
func LoadToolsFromInventory() []Category {
	categories := []Category{
		{
			Name:    "🤖 Agents",
			Purpose: "AI-powered agents for code review, testing, and deployment",
			Tools: []Tool{
				{
					Name:        "Code Reviewer",
					Purpose:     "Static code analysis and quality checks",
					Command:     "python cli.py review <file>",
					Status:      "✅ Active",
					Description: "Analyzes code for TODO/FIXME comments, line length violations, and readability issues",
					Features:    []string{"TODO/FIXME detection", "Line length validation", "File readability analysis"},
				},
				{
					Name:        "Tester",
					Purpose:     "Automated test discovery and execution",
					Command:     "python cli.py test",
					Status:      "✅ Active",
					Description: "Finds and runs test files for Python and JavaScript projects",
					Features:    []string{"Test discovery", "pytest support", "npm test support", "Pass/fail reporting"},
				},
				{
					Name:        "Deployer",
					Purpose:     "Automated deployment pipeline",
					Command:     "python cli.py deploy [branch]",
					Status:      "✅ Active",
					Description: "Automates git-based deployment with build script execution",
					Features:    []string{"Git checkout", "Build execution", "Production push"},
				},
			},
			Active: true,
		},
		{
			Name:    "🛠️ Tools",
			Purpose: "Core utilities for development and system management",
			Tools: []Tool{
				{
					Name:        "Hierarchical Memory",
					Purpose:     "Advanced SQLite-based memory management",
					Command:     "python cli.py hierarchical_memory <action>",
					Status:      "✅ Active",
					Description: "Advanced memory system with hierarchical organization and semantic relationships",
					Features:    []string{"Hierarchical nodes", "Semantic relationships", "Tag-based search", "Auto-categorization"},
				},
				{
					Name:        "Memory Manager",
					Purpose:     "Basic conversation memory storage",
					Command:     "python cli.py memory <action>",
					Status:      "✅ Active",
					Description: "Simple session-based conversation storage with SQLite persistence",
					Features:    []string{"Session storage", "SQLite persistence", "CRUD operations"},
				},
				{
					Name:        "Code Analyzer",
					Purpose:     "Comprehensive code metrics and analysis",
					Command:     "python cli.py analyze_code <action>",
					Status:      "✅ Active",
					Description: "Multi-language code analysis with complexity metrics and change detection",
					Features:    []string{"Multi-language support", "Line counting", "Complexity metrics", "File hashing"},
				},
				{
					Name:        "OpenAPI Validator",
					Purpose:     "OpenAPI specification validation",
					Command:     "python cli.py validate_openapi <spec>",
					Status:      "✅ Active",
					Description: "Validates OpenAPI specifications for required fields and structure",
					Features:    []string{"Required field validation", "Schema verification", "Extensible rules"},
				},
				{
					Name:        "Project Manager",
					Purpose:     "Project template creation and management",
					Command:     "python cli.py create_project <action>",
					Status:      "✅ Active",
					Description: "Creates project scaffolding for multiple languages and frameworks",
					Features:    []string{"Multi-language templates", "Automated scaffolding", "Configurable paths"},
				},
				{
					Name:        "Data Fetcher",
					Purpose:     "HTTP data retrieval and API interaction",
					Command:     "python cli.py fetch_data <url>",
					Status:      "✅ Active",
					Description: "Fetches data from APIs with JSON response handling and custom headers",
					Features:    []string{"JSON API handling", "Custom headers", "Error handling"},
				},
				{
					Name:        "Format Converter",
					Purpose:     "JSON formatting and conversion",
					Command:     "python cli.py convert_format <input> <output>",
					Status:      "✅ Active",
					Description: "Formats and converts JSON files with pretty-printing",
					Features:    []string{"Pretty-print formatting", "File conversion", "Indentation control"},
				},
			},
			Active: true,
		},
		{
			Name:    "🌐 MCP Servers",
			Purpose: "Model Context Protocol servers for various integrations",
			Tools: []Tool{
				{
					Name:        "Filesystem Server",
					Purpose:     "Local file system access and management",
					Command:     "python3 local_mcp_servers.py test",
					Status:      "✅ Working",
					Description: "Provides file system access to specified directories",
					Features:    []string{"File listing", "File reading", "Directory navigation"},
				},
				{
					Name:        "Memory Server",
					Purpose:     "Hierarchical memory management via MCP",
					Command:     "python3 local_mcp_servers.py test",
					Status:      "✅ Working",
					Description: "MCP interface to the hierarchical memory system",
					Features:    []string{"Session creation", "Conversation storage", "Tag search", "Hierarchy access"},
				},
				{
					Name:        "Git Server",
					Purpose:     "Git repository operations and management",
					Command:     "python3 local_mcp_servers.py test",
					Status:      "✅ Working",
					Description: "Provides git operations for the local repository",
					Features:    []string{"Git status", "Commit log", "Branch listing"},
				},
				{
					Name:        "Cloud MCP Servers",
					Purpose:     "20+ cloud-based MCP servers ready for installation",
					Command:     "python3 mcp_manager.py list",
					Status:      "🚀 Ready to Install",
					Description: "Cloud MCP servers for various services and integrations",
					Features:    []string{"GitHub integration", "Database access", "Web automation", "Infrastructure management"},
				},
			},
			Active: true,
		},
		{
			Name:    "📦 Extensions",
			Purpose: "Downloaded extensions for enhanced functionality",
			Tools: []Tool{
				{
					Name:        "OpenCode MCP Tool",
					Purpose:     "Direct OpenCode CLI integration with multi-model support",
					Command:     "cd extensions/opencode-mcp-tool && npm install",
					Status:      "✅ Ready",
					Description: "TypeScript/Node.js extension for OpenCode CLI integration",
					Features:    []string{"Natural language processing", "Multi-model AI", "Tool registry", "Slash commands"},
				},
				{
					Name:        "AI Sessions MCP",
					Purpose:     "Cross-AI session search and management",
					Command:     "cd extensions/ai-sessions-mcp && go install",
					Status:      "✅ Ready",
					Description: "Go-based extension for cross-AI session management",
					Features:    []string{"Claude integration", "Gemini support", "BM25 search", "Session caching"},
				},
				{
					Name:        "LLMs",
					Purpose:     "Centralized LLM configuration with Feature-Implementer v2",
					Command:     "cd extensions/llms && pip install -e .",
					Status:      "✅ Ready",
					Description: "Python-based centralized LLM management system",
					Features:    []string{"Multi-LLM support", "Agent builder", "Async execution", "Test suite"},
				},
				{
					Name:        "System Prompt Orchestrator",
					Purpose:     "Multi-agent workflow coordination",
					Command:     "cd extensions/systemprompt-code-orchestrator && pip install -e .",
					Status:      "✅ Ready",
					Description: "Python framework for multi-agent workflow coordination",
					Features:    []string{"Agent composition", "Workflow management", "System prompts"},
				},
				{
					Name:        "FastMCP",
					Purpose:     "Rapid MCP server development framework",
					Command:     "cd extensions/fastmcp && pip install -e .",
					Status:      "✅ Ready",
					Description: "Python framework for rapid MCP server development",
					Features:    []string{"Quick scaffolding", "Prompt management", "Testing utilities"},
				},
				{
					Name:        "MCP-Box",
					Purpose:     "Universal MCP management tool",
					Command:     "cd extensions/mcp-box && npm install",
					Status:      "✅ Ready",
					Description: "TypeScript/Node.js universal MCP management tool",
					Features:    []string{"Server registry", "Security utilities", "Configuration management"},
				},
			},
			Active: true,
		},
		{
			Name:    "🔗 Integrations",
			Purpose: "External service integrations and automation",
			Tools: []Tool{
				{
					Name:        "Automation",
					Purpose:     "GitHub issue automation and management",
					Command:     "python cli.py automate <action>",
					Status:      "✅ Configured",
					Description: "Automates GitHub issue creation and management with token support",
					Features:    []string{"GitHub integration", "Token management", "Issue automation"},
				},
				{
					Name:        "Webhook Handler",
					Purpose:     "Multi-platform webhook processing",
					Command:     "python cli.py handle_webhook <action>",
					Status:      "✅ Configured",
					Description: "Handles webhooks from GitHub, GitLab, and Linear",
					Features:    []string{"Multi-platform support", "Webhook processing", "Issue creation"},
				},
				{
					Name:        "Linear Manager",
					Purpose:     "Linear project management integration",
					Command:     "python cli.py manage_linear <action>",
					Status:      "✅ Configured",
					Description: "Integrates with Linear for project and issue management",
					Features:    []string{"Linear API", "Issue tracking", "Project management"},
				},
			},
			Active: true,
		},
		{
			Name:    "⚙️ Configs",
			Purpose: "Configuration management and security tools",
			Tools: []Tool{
				{
					Name:        "FOSS Token Manager",
					Purpose:     "Secure FOSS-compliant token storage",
					Command:     "python cli.py foss_token <action>",
					Status:      "✅ Active",
					Description: "Secure token storage with Fernet encryption and local storage",
					Features:    []string{"Fernet encryption", "Local storage", "Token rotation", "Export/import"},
				},
				{
					Name:        "Memory Config",
					Purpose:     "Memory system configuration management",
					Command:     "python cli.py memory_config <action>",
					Status:      "✅ Active",
					Description: "Configuration management for the memory system",
					Features:    []string{"Database settings", "Retention policies", "Performance tuning"},
				},
				{
					Name:        "Token Manager",
					Purpose:     "Legacy token management system",
					Command:     "python cli.py get_token <action>",
					Status:      "✅ Active",
					Description: "Basic token management system",
					Features:    []string{"Basic storage", "Service organization"},
				},
			},
			Active: true,
		},
	}

	return categories
}

// ExecuteCommand runs a command and returns its output
func ExecuteCommand(command string) (string, error) {
	parts := strings.Fields(command)
	if len(parts) == 0 {
		return "", fmt.Errorf("empty command")
	}

	cmd := exec.Command(parts[0], parts[1:]...)
	cmd.Dir = "/home/cbwinslow/opencode_extensions"

	output, err := cmd.CombinedOutput()
	if err != nil {
		return string(output), err
	}

	return string(output), nil
}

// GetWorkingDirectory returns the current working directory
func GetWorkingDirectory() string {
	dir, err := os.Getwd()
	if err != nil {
		return "/home/cbwinslow/opencode_extensions"
	}
	return dir
}

// ReadFileContent reads the content of a file
func ReadFileContent(filepath string) (string, error) {
	content, err := os.ReadFile(filepath)
	if err != nil {
		return "", err
	}
	return string(content), nil
}

// WriteFileContent writes content to a file
func WriteFileContent(filepath, content string) error {
	return os.WriteFile(filepath, []byte(content), 0644)
}

// PromptUser prompts the user for input
func PromptUser(prompt string) string {
	fmt.Print(prompt)
	reader := bufio.NewReader(os.Stdin)
	text, _ := reader.ReadString('\n')
	return strings.TrimSpace(text)
}
