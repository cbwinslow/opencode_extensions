package main

import (
	"fmt"
	"os"

	tea "github.com/charmbracelet/bubbletea"
)

func main() {
	// Check if we're in the right directory
	if _, err := os.Stat("../cli.py"); os.IsNotExist(err) {
		fmt.Println("Error: Please run this tool from the tools-tui directory")
		fmt.Println("The TUI expects to find the OpenCode tools in the parent directory")
		os.Exit(1)
	}

	// Initialize and start the TUI
	p := tea.NewProgram(InitialModel(), tea.WithAltScreen())
	if _, err := p.Run(); err != nil {
		fmt.Printf("Error running TUI: %v", err)
		os.Exit(1)
	}
}
