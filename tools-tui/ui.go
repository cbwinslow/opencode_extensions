package main

import (
	"fmt"
	"strings"

	"github.com/charmbracelet/bubbles/help"
	"github.com/charmbracelet/bubbles/key"
	"github.com/charmbracelet/bubbles/textinput"
	"github.com/charmbracelet/bubbles/viewport"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

// Styles for the TUI
var (
	titleStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FAFAFA")).
			Background(lipgloss.Color("#7D56F4")).
			Padding(0, 1)

	statusStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#FAFAFA")).
			Background(lipgloss.Color("#F25D94")).
			Padding(0, 1)

	selectedItemStyle = lipgloss.NewStyle().
				Foreground(lipgloss.Color("#EE6FF8")).
				Bold(true)

	descriptionStyle = lipgloss.NewStyle().
				Foreground(lipgloss.Color("#DFDFDF"))

	featureStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#7FD5F2")).
			Bold(true)

	commandStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#A8F0A0")).
			Background(lipgloss.Color("#1A1A1A")).
			Padding(0, 1)

	helpStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#626262"))

	footerStyle = lipgloss.NewStyle().
			Foreground(lipgloss.Color("#DFDFDF")).
			Background(lipgloss.Color("#1A1A1A"))
)

// KeyMap defines key bindings
type KeyMap struct {
	Up             key.Binding
	Down           key.Binding
	Left           key.Binding
	Right          key.Binding
	Enter          key.Binding
	Back           key.Binding
	Search         key.Binding
	Execute        key.Binding
	Help           key.Binding
	Quit           key.Binding
	ToggleCategory key.Binding
}

// ShortHelp returns keybindings for the help menu
func (k KeyMap) ShortHelp() []key.Binding {
	return []key.Binding{k.Help, k.Quit}
}

// FullHelp returns keybindings for the expanded help menu
func (k KeyMap) FullHelp() [][]key.Binding {
	return [][]key.Binding{
		{k.Up, k.Down, k.Left, k.Right},
		{k.Enter, k.Back, k.Search, k.Execute},
		{k.ToggleCategory, k.Help, k.Quit},
	}
}

// DefaultKeyMap returns the default key bindings
func DefaultKeyMap() KeyMap {
	return KeyMap{
		Up: key.NewBinding(
			key.WithKeys("up", "k"),
			key.WithHelp("↑/k", "move up"),
		),
		Down: key.NewBinding(
			key.WithKeys("down", "j"),
			key.WithHelp("↓/j", "move down"),
		),
		Left: key.NewBinding(
			key.WithKeys("left", "h"),
			key.WithHelp("←/h", "previous category"),
		),
		Right: key.NewBinding(
			key.WithKeys("right", "l"),
			key.WithHelp("→/l", "next category"),
		),
		Enter: key.NewBinding(
			key.WithKeys("enter", " "),
			key.WithHelp("enter/space", "select tool"),
		),
		Back: key.NewBinding(
			key.WithKeys("esc", "q"),
			key.WithHelp("esc/q", "back"),
		),
		Search: key.NewBinding(
			key.WithKeys("/"),
			key.WithHelp("/", "search"),
		),
		Execute: key.NewBinding(
			key.WithKeys("x"),
			key.WithHelp("x", "execute command"),
		),
		Help: key.NewBinding(
			key.WithKeys("?"),
			key.WithHelp("?", "toggle help"),
		),
		Quit: key.NewBinding(
			key.WithKeys("ctrl+c", "Q"),
			key.WithHelp("ctrl+c/Q", "quit"),
		),
		ToggleCategory: key.NewBinding(
			key.WithKeys("tab"),
			key.WithHelp("tab", "toggle category"),
		),
	}
}

// Model represents the application state
type Model struct {
	categories    []Category
	currentCat    int
	currentTool   int
	searchInput   textinput.Model
	viewport      viewport.Model
	help          help.Model
	keys          KeyMap
	showHelp      bool
	searchMode    bool
	detailMode    bool
	selectedTool  *Tool
	commandOutput string
	width         int
	height        int
}

// InitialModel returns the initial model
func InitialModel() Model {
	si := textinput.New()
	si.Placeholder = "Search tools..."
	si.CharLimit = 156
	si.Width = 50

	v := viewport.New(50, 20)
	v.SetContent("")

	help := help.New()
	help.ShowAll = false

	categories := LoadToolsFromInventory()

	return Model{
		categories:  categories,
		currentCat:  0,
		currentTool: 0,
		searchInput: si,
		viewport:    v,
		help:        help,
		keys:        DefaultKeyMap(),
		showHelp:    false,
		searchMode:  false,
		detailMode:  false,
		width:       100,
		height:      30,
	}
}

// Init initializes the model
func (m Model) Init() tea.Cmd {
	return textinput.Blink
}

// Update handles updates to the model
func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd

	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
		m.viewport.Width = msg.Width - 20
		m.viewport.Height = msg.Height - 15
		m.searchInput.Width = msg.Width - 40

	case tea.KeyMsg:
		switch {
		case key.Matches(msg, m.keys.Quit):
			return m, tea.Quit

		case key.Matches(msg, m.keys.Help):
			m.showHelp = !m.showHelp
			m.help.ShowAll = m.showHelp

		case key.Matches(msg, m.keys.Search):
			m.searchMode = true
			m.searchInput.Focus()
			return m, textinput.Blink

		case key.Matches(msg, m.keys.Back):
			if m.searchMode {
				m.searchMode = false
				m.searchInput.Blur()
				m.searchInput.SetValue("")
			} else if m.detailMode {
				m.detailMode = false
				m.selectedTool = nil
				m.commandOutput = ""
			}

		case key.Matches(msg, m.keys.Execute):
			if m.detailMode && m.selectedTool != nil {
				output, err := ExecuteCommand(m.selectedTool.Command)
				if err != nil {
					m.commandOutput = fmt.Sprintf("Error: %v\n\nOutput:\n%s", err, output)
				} else {
					m.commandOutput = output
				}
				m.viewport.SetContent(m.commandOutput)
				m.viewport.GotoTop()
			}

		case key.Matches(msg, m.keys.Enter):
			if m.searchMode {
				m.searchMode = false
				m.searchInput.Blur()
				// Search logic would go here
			} else if !m.detailMode {
				// Enter detail mode
				currentCategory := m.categories[m.currentCat]
				if len(currentCategory.Tools) > 0 {
					m.selectedTool = &currentCategory.Tools[m.currentTool]
					m.detailMode = true
					m.commandOutput = ""
					m.viewport.SetContent("")
				}
			}

		case key.Matches(msg, m.keys.Up):
			if !m.detailMode && !m.searchMode {
				if m.currentTool > 0 {
					m.currentTool--
				}
			}

		case key.Matches(msg, m.keys.Down):
			if !m.detailMode && !m.searchMode {
				currentCategory := m.categories[m.currentCat]
				if m.currentTool < len(currentCategory.Tools)-1 {
					m.currentTool++
				}
			}

		case key.Matches(msg, m.keys.Left):
			if !m.detailMode && !m.searchMode {
				if m.currentCat > 0 {
					m.currentCat--
					m.currentTool = 0
				}
			}

		case key.Matches(msg, m.keys.Right):
			if !m.detailMode && !m.searchMode {
				if m.currentCat < len(m.categories)-1 {
					m.currentCat++
					m.currentTool = 0
				}
			}

		case key.Matches(msg, m.keys.ToggleCategory):
			if !m.detailMode && !m.searchMode {
				// Toggle category visibility
				if m.currentCat < len(m.categories) {
					m.categories[m.currentCat].Active = !m.categories[m.currentCat].Active
				}
			}
		}
	}

	// Update search input if in search mode
	if m.searchMode {
		m.searchInput, cmd = m.searchInput.Update(msg)
	}

	// Update viewport for scrolling
	if m.detailMode {
		m.viewport, cmd = m.viewport.Update(msg)
	}

	return m, cmd
}

// View renders the model
func (m Model) View() string {
	if m.detailMode && m.selectedTool != nil {
		return m.renderDetailView()
	}

	// Header
	title := titleStyle.Render("🛠️  OpenCode Tools & Plugins TUI")
	status := statusStyle.Render(fmt.Sprintf("%d Tools | %d Categories", m.getTotalTools(), len(m.categories)))
	header := lipgloss.JoinHorizontal(lipgloss.Center, title, "  ", status)

	// Main content
	mainContent := m.renderMainView()

	// Footer
	footer := m.renderFooter()

	// Help section
	helpView := ""
	if m.showHelp {
		helpView = m.help.View(m.keys)
	}

	// Combine all sections
	content := lipgloss.JoinVertical(lipgloss.Left,
		header,
		"",
		mainContent,
		"",
		footer,
	)

	if helpView != "" {
		content = lipgloss.JoinVertical(lipgloss.Left,
			content,
			"",
			helpStyle.Render(helpView),
		)
	}

	return content
}

// renderMainView renders the main list view
func (m Model) renderMainView() string {
	var content strings.Builder

	// Categories and tools
	for i, category := range m.categories {
		// Category header
		catStyle := titleStyle
		if i == m.currentCat && !m.searchMode {
			catStyle = catStyle.Copy().Background(lipgloss.Color("#EE6FF8"))
		}

		categoryLine := fmt.Sprintf("%s %s (%d tools)",
			catStyle.Render(category.Name),
			descriptionStyle.Render("- "+category.Purpose),
			len(category.Tools))

		content.WriteString(categoryLine)
		content.WriteString("\n")

		// Tools in category
		if category.Active {
			for j, tool := range category.Tools {
				toolPrefix := "  "
				if i == m.currentCat && j == m.currentTool && !m.searchMode {
					toolPrefix = "▶ "
					toolName := selectedItemStyle.Render(tool.Name)
					toolStatus := statusStyle.Render(tool.Status)
					toolLine := fmt.Sprintf("%s%s %s - %s",
						toolPrefix, toolName, toolStatus,
						descriptionStyle.Render(tool.Purpose))
					content.WriteString(toolLine)
				} else {
					toolLine := fmt.Sprintf("%s• %s %s - %s",
						toolPrefix, tool.Name, tool.Status,
						descriptionStyle.Render(tool.Purpose))
					content.WriteString(toolLine)
				}
				content.WriteString("\n")
			}
		}
		content.WriteString("\n")
	}

	// Search input
	if m.searchMode {
		searchLine := fmt.Sprintf("🔍 %s", m.searchInput.View())
		content.WriteString(commandStyle.Render(searchLine))
	}

	return content.String()
}

// renderDetailView renders the detailed view for a selected tool
func (m Model) renderDetailView() string {
	if m.selectedTool == nil {
		return "No tool selected"
	}

	var content strings.Builder

	// Tool header
	title := titleStyle.Render(m.selectedTool.Name)
	status := statusStyle.Render(m.selectedTool.Status)
	header := lipgloss.JoinHorizontal(lipgloss.Center, title, "  ", status)
	content.WriteString(header)
	content.WriteString("\n\n")

	// Tool details
	content.WriteString(descriptionStyle.Bold(true).Render("Purpose: "))
	content.WriteString(m.selectedTool.Purpose)
	content.WriteString("\n\n")

	content.WriteString(descriptionStyle.Bold(true).Render("Description: "))
	content.WriteString(m.selectedTool.Description)
	content.WriteString("\n\n")

	content.WriteString(descriptionStyle.Bold(true).Render("Command: "))
	content.WriteString(commandStyle.Render(m.selectedTool.Command))
	content.WriteString("\n\n")

	// Features
	if len(m.selectedTool.Features) > 0 {
		content.WriteString(descriptionStyle.Bold(true).Render("Features:\n"))
		for _, feature := range m.selectedTool.Features {
			content.WriteString(fmt.Sprintf("  %s %s\n", featureStyle.Render("•"), feature))
		}
		content.WriteString("\n")
	}

	// Command output
	if m.commandOutput != "" {
		content.WriteString(descriptionStyle.Bold(true).Render("Command Output:\n"))
		content.WriteString(m.viewport.View())
	}

	// Instructions
	instructions := "Press 'x' to execute command, 'esc' to go back, '?' for help"
	content.WriteString("\n")
	content.WriteString(helpStyle.Render(instructions))

	return content.String()
}

// renderFooter renders the footer
func (m Model) renderFooter() string {
	var instructions []string

	if m.detailMode {
		instructions = []string{"x: execute", "esc: back", "↑/↓: scroll", "?: help", "ctrl+c: quit"}
	} else if m.searchMode {
		instructions = []string{"enter: search", "esc: cancel", "?: help", "ctrl+c: quit"}
	} else {
		instructions = []string{
			"↑/↓: navigate", "←/→: categories", "enter: details",
			"/: search", "tab: toggle", "x: execute", "?: help", "ctrl+c: quit",
		}
	}

	return footerStyle.Render(strings.Join(instructions, " | "))
}

// getTotalTools returns the total number of tools across all categories
func (m Model) getTotalTools() int {
	total := 0
	for _, category := range m.categories {
		total += len(category.Tools)
	}
	return total
}
