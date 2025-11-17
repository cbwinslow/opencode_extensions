#!/bin/bash

# Multi-Agent System Setup Script
# Installs dependencies and verifies environment

set -e

echo "=========================================="
echo "Multi-Agent System Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Error: Python 3 not found"; exit 1; }
echo "✓ Python 3 found"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
echo "✓ Python dependencies installed"
echo ""

# Check for Redis
echo "Checking for Redis..."
if command -v redis-server &> /dev/null; then
    echo "✓ Redis found"
    redis-cli ping &> /dev/null && echo "✓ Redis is running" || echo "⚠ Redis is installed but not running. Start with: redis-server"
else
    echo "⚠ Redis not found. Install Redis for agent communication:"
    echo "  Ubuntu/Debian: sudo apt-get install redis-server"
    echo "  macOS: brew install redis"
    echo "  Or use Docker: docker run -d -p 6379:6379 redis:latest"
fi
echo ""

# Create data directories
echo "Creating data directories..."
mkdir -p chroma_data
mkdir -p vector_data
echo "✓ Data directories created"
echo ""

# Test vector database
echo "Testing vector database..."
python3 -c "from tools.vector_database import VectorDatabaseManager; db = VectorDatabaseManager(); print('✓ ChromaDB working')" || echo "⚠ ChromaDB test failed"
echo ""

# Test agent communication (if Redis is available)
echo "Testing agent communication..."
if redis-cli ping &> /dev/null; then
    python3 -c "from tools.agent_communication import AgentCommunicationHub; hub = AgentCommunicationHub(); print('✓ Agent communication working')" || echo "⚠ Agent communication test failed"
else
    echo "⚠ Skipping agent communication test (Redis not running)"
fi
echo ""

# Display next steps
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Start Redis (if not running):"
echo "   redis-server"
echo ""
echo "2. Run the demo:"
echo "   python3 demo_multiagent.py"
echo ""
echo "3. Try CLI commands:"
echo "   python3 cli.py vector_db init chromadb"
echo "   python3 cli.py agent_comm health"
echo "   python3 cli.py multiagent demo"
echo ""
echo "4. Read the guide:"
echo "   cat MULTIAGENT_GUIDE.md"
echo ""
echo "For full documentation, see MULTIAGENT_GUIDE.md"
echo ""
