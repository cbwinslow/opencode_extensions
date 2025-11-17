# Multi-Agent System - Example Use Cases

## Real-World Applications

This document provides practical examples of using the multi-agent democratic problem-solving system.

## Example 1: Code Review by Democratic Consensus

### Scenario
Multiple AI agents review code changes and reach consensus on whether to approve.

### Implementation

```python
from agents.multiagent_coordinator import MultiAgentCoordinator, ProblemSolvingStrategy
from tools.vector_database import VectorDatabaseManager

# Initialize system
coordinator = MultiAgentCoordinator()
coordinator.spawn_agents(count=5, role_distribution={
    AgentRole.PROBLEM_SOLVER: 3,
    AgentRole.NOTE_TAKER: 1,
    AgentRole.MONITOR: 1
})

# Load code review guidelines into vector DB
vector_db = coordinator.vector_db
vector_db.ingest_file("code_review_guidelines.md")

# Agents review code and vote
solution = coordinator.solve_problem(
    "Review PR #123: Add authentication middleware",
    ProblemSolvingStrategy.CONSENSUS,
    context={
        "pr_number": 123,
        "files_changed": ["middleware/auth.py"],
        "guidelines": vector_db.search("authentication best practices", top_k=3)
    }
)

print(f"Consensus reached: {solution['consensus_reached']}")
print(f"Agreement: {solution['agreement_percent']:.1%}")
```

## Example 2: Task Allocation with Auction System

### Scenario
Distribute multiple tasks among agents based on their capabilities and current load.

### Implementation

```python
# Define tasks
tasks = [
    {"name": "Optimize database queries", "complexity": 8, "priority": "high"},
    {"name": "Write unit tests", "complexity": 5, "priority": "medium"},
    {"name": "Update documentation", "complexity": 3, "priority": "low"},
    {"name": "Fix bug in authentication", "complexity": 7, "priority": "critical"}
]

# Allocate each task via auction
coordinator = MultiAgentCoordinator()
coordinator.spawn_agents(count=6)

results = []
for task in tasks:
    solution = coordinator.solve_problem(
        f"Execute task: {task['name']}",
        ProblemSolvingStrategy.AUCTION,
        context=task
    )
    results.append(solution)

# Display allocation
for task, solution in zip(tasks, results):
    print(f"{task['name']} → Agent {solution['winner_agent']}")
```

## Example 3: Swarm-Based Bug Detection

### Scenario
Multiple agents analyze codebase in parallel to find potential bugs.

### Implementation

```python
import os
from pathlib import Path

coordinator = MultiAgentCoordinator()
coordinator.spawn_agents(count=10)  # Swarm of 10 agents

# Find all Python files
code_files = list(Path("src").rglob("*.py"))

# Store files in vector DB for semantic search
for file in code_files:
    coordinator.vector_db.ingest_file(str(file))

# Swarm analyzes for common bug patterns
solution = coordinator.solve_problem(
    "Find potential bugs: null references, race conditions, memory leaks",
    ProblemSolvingStrategy.SWARM,
    context={
        "files": [str(f) for f in code_files],
        "patterns": ["null check", "thread safety", "resource cleanup"]
    }
)

print(f"Analyzed by {solution['results_count']} agents")
print(f"Potential issues found: {len(solution.get('issues', []))}")
```

## Example 4: Hierarchical System Design

### Scenario
Break down complex system design into components, design each, then integrate.

### Implementation

```python
coordinator = MultiAgentCoordinator()
coordinator.spawn_agents(count=8)

# High-level system design problem
problem = """
Design a distributed e-commerce platform with:
- User authentication
- Product catalog
- Shopping cart
- Payment processing
- Order management
- Inventory tracking
"""

# Hierarchical decomposition and solution
solution = coordinator.solve_problem(
    problem,
    ProblemSolvingStrategy.HIERARCHICAL,
    context={
        "requirements": ["scalability", "fault-tolerance", "security"],
        "constraints": ["microservices", "FOSS only", "cloud-native"]
    }
)

print(f"System broken into {solution['sub_problems_count']} components")
print(f"Sub-solutions: {len(solution['sub_solutions'])}")
print(f"Final architecture: {solution['final_solution']}")
```

## Example 5: Multi-Round Debate for Architecture Decisions

### Scenario
Agents debate different architectural approaches and refine through discussion.

### Implementation

```python
coordinator = MultiAgentCoordinator()
coordinator.spawn_agents(count=5, role_distribution={
    AgentRole.PROBLEM_SOLVER: 4,  # 4 debaters
    AgentRole.NOTE_TAKER: 1       # 1 note-taker to document debate
})

# Contentious architecture decision
problem = """
Choose database architecture:
Option A: Single PostgreSQL with read replicas
Option B: Microservices with per-service databases
Option C: Distributed database (CockroachDB)
"""

solution = coordinator.solve_problem(
    problem,
    ProblemSolvingStrategy.DEBATE,
    context={
        "factors": ["scalability", "consistency", "operational complexity", "cost"],
        "constraints": ["team size: 5 developers", "budget: limited", "timeline: 6 months"]
    }
)

print(f"Debate rounds: {solution['debate_rounds']}")
print(f"Arguments generated: {solution['solutions_generated']}")
print(f"Winner: {solution['winner']}")

# Retrieve debate notes
notes = coordinator.hub.get_message_history(limit=50)
debate_notes = [n for n in notes if n.get('message_type') == 'note_taking']
print(f"Detailed notes available: {len(debate_notes)} entries")
```

## Example 6: Knowledge Base with Semantic Search

### Scenario
Build a searchable knowledge base from documentation and code.

### Implementation

```python
from tools.vector_database import VectorDatabaseManager

# Initialize vector database
vector_db = VectorDatabaseManager(db_type="chromadb", config={
    "persist_directory": "./knowledge_base",
    "collection_name": "project_knowledge"
})

# Ingest documentation
docs = [
    "README.md",
    "ARCHITECTURE.md",
    "API_REFERENCE.md",
    "docs/guides/getting-started.md",
    "docs/guides/advanced-usage.md"
]

for doc in docs:
    if os.path.exists(doc):
        print(f"Ingesting {doc}...")
        vector_db.ingest_file(doc, chunk_size=500, overlap=50)

# Search knowledge base
queries = [
    "How do I configure authentication?",
    "What are the performance best practices?",
    "How to deploy to production?"
]

for query in queries:
    print(f"\nQuery: {query}")
    results = vector_db.search(query, top_k=3)
    
    for i, result in enumerate(results):
        print(f"  {i+1}. {result['metadata'].get('source', 'Unknown')}")
        print(f"     Score: {result['score']:.4f}")
        print(f"     {result['content'][:100]}...")

# Get statistics
stats = vector_db.get_stats()
print(f"\nKnowledge base contains {stats['document_count']} chunks")
```

## Example 7: Self-Healing System Monitor

### Scenario
Monitor agent watches system health and healer agents fix issues automatically.

### Implementation

```python
import time
import threading

coordinator = MultiAgentCoordinator()
coordinator.spawn_agents(count=4, role_distribution={
    AgentRole.MONITOR: 1,
    AgentRole.HEALER: 2,
    AgentRole.NOTE_TAKER: 1
})

# Monitor runs continuously
def monitoring_loop():
    while True:
        # Check system health
        health = coordinator.hub.health_check()
        
        if health['status'] != 'healthy':
            print("⚠ System issue detected!")
            
            # Request healing
            coordinator.hub.send_message(
                MessageType.HELP_REQUEST,
                {
                    "issue": "system_unhealthy",
                    "details": health
                },
                recipient_role=AgentRole.HEALER
            )
        
        # Check agent health
        agents = coordinator.hub.get_agent_status()
        dead_agents = [aid for aid, info in agents.items() if not info['is_alive']]
        
        if dead_agents:
            print(f"⚠ {len(dead_agents)} agents are not responding")
            
            # Alert about dead agents
            coordinator.hub.send_message(
                MessageType.MONITOR_ALERT,
                {
                    "alert": "agents_dead",
                    "dead_agents": dead_agents
                }
            )
        
        time.sleep(10)  # Check every 10 seconds

# Start monitoring in background
monitor_thread = threading.Thread(target=monitoring_loop, daemon=True)
monitor_thread.start()

# System continues operating while monitored
print("System monitoring active. Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nMonitoring stopped")
```

## Example 8: Collaborative Document Analysis

### Scenario
Multiple agents analyze documents and build structured knowledge graph.

### Implementation

```python
coordinator = MultiAgentCoordinator()
coordinator.spawn_agents(count=6)

# Documents to analyze
documents = [
    "requirements.txt",
    "architecture_diagram.pdf",
    "meeting_notes.md",
    "technical_spec.docx"
]

# Each agent analyzes subset of documents
for doc in documents:
    coordinator.vector_db.ingest_file(doc)

# Agents collaborate to extract key concepts
solution = coordinator.solve_problem(
    "Extract and categorize key concepts from project documents",
    ProblemSolvingStrategy.SWARM,
    context={
        "documents": documents,
        "categories": ["requirements", "architecture", "decisions", "risks"]
    }
)

# Build knowledge graph
from tools.hierarchical_memory import HierarchicalMemoryManager
memory = HierarchicalMemoryManager()

# Store concepts in hierarchical memory
concepts_root = memory.create_node("concepts_root", "Project Concepts", weight=3.0)

for concept in solution.get('concepts', []):
    memory.create_concept_node(
        concept['name'],
        concept['definition'],
        tags=concept.get('categories', [])
    )

print("Knowledge graph built with hierarchical relationships")
```

## Example 9: Real-Time Problem Solving Dashboard

### Scenario
Web dashboard showing multi-agent system solving problems in real-time.

### Implementation

```python
from flask import Flask, jsonify, render_template
import threading

app = Flask(__name__)
coordinator = MultiAgentCoordinator()
coordinator.spawn_agents(count=8)

@app.route('/api/status')
def get_status():
    return jsonify(coordinator.get_system_status())

@app.route('/api/solve', methods=['POST'])
def solve_problem():
    from flask import request
    
    data = request.json
    problem = data.get('problem')
    strategy = ProblemSolvingStrategy[data.get('strategy', 'VOTING').upper()]
    
    # Solve in background
    def solve():
        solution = coordinator.solve_problem(problem, strategy)
        # Store solution for retrieval
        coordinator.active_problems[solution['problem_id']] = solution
    
    thread = threading.Thread(target=solve)
    thread.start()
    
    return jsonify({"status": "solving"})

@app.route('/api/agents')
def get_agents():
    status = coordinator.hub.get_agent_status()
    return jsonify(status)

@app.route('/api/votes')
def get_votes():
    # Get recent votes from message history
    history = coordinator.hub.get_message_history(limit=100)
    votes = [m for m in history if m.get('message_type') == 'vote_request']
    return jsonify(votes)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Example 10: Integration with Existing Systems

### Scenario
Integrate multi-agent system with existing CI/CD pipeline.

### Implementation

```python
# In your CI/CD script (e.g., .github/workflows/main.yml or Jenkins)

from agents.multiagent_coordinator import MultiAgentCoordinator, ProblemSolvingStrategy

def ci_cd_integration():
    coordinator = MultiAgentCoordinator()
    coordinator.spawn_agents(count=5)
    
    # 1. Code review by consensus
    review = coordinator.solve_problem(
        "Review changes in PR",
        ProblemSolvingStrategy.CONSENSUS,
        context={
            "files_changed": get_changed_files(),
            "diff": get_git_diff()
        }
    )
    
    if not review['consensus_reached']:
        print("❌ Code review consensus not reached")
        exit(1)
    
    # 2. Allocate tests to agents
    test_solution = coordinator.solve_problem(
        "Run test suite in parallel",
        ProblemSolvingStrategy.AUCTION,
        context={
            "test_files": get_test_files(),
            "parallel_jobs": 5
        }
    )
    
    # 3. Democratic decision on deployment
    deploy_vote = coordinator.solve_problem(
        "Approve deployment to production?",
        ProblemSolvingStrategy.VOTING,
        context={
            "build_status": "passed",
            "test_coverage": "95%",
            "security_scan": "clean"
        }
    )
    
    if deploy_vote['winner'] == 'approve':
        print("✅ Deployment approved by agents")
        # Proceed with deployment
    else:
        print("❌ Deployment rejected by agents")
        exit(1)

if __name__ == "__main__":
    ci_cd_integration()
```

## Tips for Real-World Usage

### 1. Choose the Right Strategy

- **VOTING**: Quick decisions, multiple options
- **CONSENSUS**: Important decisions requiring agreement
- **AUCTION**: Resource allocation, load balancing
- **SWARM**: Exploration, parallel processing
- **DEBATE**: Complex decisions needing analysis
- **HIERARCHICAL**: Large problems with clear decomposition

### 2. Optimize Agent Count

```python
# Simple problems
coordinator.spawn_agents(count=3)

# Moderate complexity
coordinator.spawn_agents(count=5-7)

# Complex problems
coordinator.spawn_agents(count=10-15)
```

### 3. Use Vector DB for Context

```python
# Store relevant knowledge
vector_db.ingest_file("best_practices.md")

# Provide context to agents
context = {
    "knowledge": vector_db.search(problem, top_k=5)
}

solution = coordinator.solve_problem(problem, strategy, context=context)
```

### 4. Monitor Performance

```python
import time

start = time.time()
solution = coordinator.solve_problem(problem, strategy)
duration = time.time() - start

print(f"Solved in {duration:.2f} seconds")
print(f"Agents used: {len(coordinator.agents)}")
```

### 5. Handle Failures Gracefully

```python
try:
    solution = coordinator.solve_problem(problem, strategy)
except Exception as e:
    print(f"Error: {e}")
    
    # Fallback to simpler strategy
    solution = coordinator.solve_problem(
        problem,
        ProblemSolvingStrategy.VOTING  # Simpler fallback
    )
```

## Conclusion

These examples demonstrate the versatility of the multi-agent system. Combine components creatively to solve your specific problems!

For more details, see:
- [MULTIAGENT_GUIDE.md](MULTIAGENT_GUIDE.md) - Complete guide
- [README.md](README.md) - Quick start
- [AGENTS.md](AGENTS.md) - Code style and conventions
