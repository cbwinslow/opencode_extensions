# Multi-Agent System - Quick Reference

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Start Redis
redis-server

# Run setup
./setup_multiagent.sh
```

## Basic Usage

### Initialize System

```python
from agents.multiagent_coordinator import MultiAgentCoordinator, ProblemSolvingStrategy

coordinator = MultiAgentCoordinator()
coordinator.spawn_agents(count=5)
```

### Solve Problem

```python
solution = coordinator.solve_problem(
    "Your problem here",
    ProblemSolvingStrategy.VOTING
)
```

## Strategies

| Strategy | Use Case | Speed | Quality |
|----------|----------|-------|---------|
| `VOTING` | Quick decisions | ⚡⚡⚡ | ⭐⭐ |
| `CONSENSUS` | Important decisions | ⚡⚡ | ⭐⭐⭐ |
| `AUCTION` | Resource allocation | ⚡⚡ | ⭐⭐⭐ |
| `SWARM` | Parallel exploration | ⚡⚡⚡ | ⭐⭐ |
| `DEBATE` | Complex analysis | ⚡ | ⭐⭐⭐⭐ |
| `HIERARCHICAL` | Large problems | ⚡⚡ | ⭐⭐⭐⭐ |

## Agent Roles

- `PROBLEM_SOLVER` - Main reasoning and execution
- `MONITOR` - System health monitoring
- `NOTE_TAKER` - Documentation and logging
- `HEALER` - Self-healing and recovery
- `COORDINATOR` - Task orchestration

## Vector Database

```python
from tools.vector_database import VectorDatabaseManager

# Initialize
vector_db = VectorDatabaseManager(db_type="chromadb")

# Ingest
doc_ids = vector_db.ingest_file("document.txt")

# Search
results = vector_db.search("query", top_k=5)
```

## Agent Communication

```python
from tools.agent_communication import AgentCommunicationHub, AgentRole

# Initialize
hub = AgentCommunicationHub()

# Register agent
hub.register_agent("agent1", AgentRole.PROBLEM_SOLVER)

# Vote
vote_data = hub.request_vote("Proposal", ["yes", "no"])
hub.cast_vote(vote_data['vote_id'], "yes")
results = hub.get_vote_results(vote_data['vote_id'])
```

## CLI Commands

```bash
# Vector DB
python cli.py vector_db init chromadb
python cli.py vector_db ingest file.txt
python cli.py vector_db search "query"

# Agent Communication
python cli.py agent_comm register agent1 problem_solver
python cli.py agent_comm status
python cli.py agent_comm health

# Multi-Agent
python cli.py multiagent demo
python cli.py multiagent spawn 5
python cli.py multiagent solve "problem" voting
```

## Configuration

### Redis Config
```python
redis_config = {
    "host": "localhost",
    "port": 6379,
    "db": 0
}
```

### Vector DB Config
```python
vector_db_config = {
    "type": "chromadb",
    "persist_directory": "./data",
    "collection_name": "docs"
}
```

### Agent Distribution
```python
role_distribution = {
    AgentRole.PROBLEM_SOLVER: 3,
    AgentRole.MONITOR: 1,
    AgentRole.NOTE_TAKER: 1,
    AgentRole.HEALER: 1
}
```

## Common Patterns

### Pattern 1: Solve with Knowledge

```python
# Add knowledge
vector_db.ingest_file("knowledge.md")

# Search for relevant info
knowledge = vector_db.search(problem, top_k=3)

# Solve with context
solution = coordinator.solve_problem(
    problem,
    strategy,
    context={"knowledge": knowledge}
)
```

### Pattern 2: Democratic Decision

```python
# Request vote
vote = hub.request_vote("Proposal", ["yes", "no", "abstain"])

# Wait for votes
time.sleep(5)

# Get results
results = hub.get_vote_results(vote['vote_id'])
winner = results['winner']
```

### Pattern 3: Task Allocation

```python
task = {"type": "analysis", "priority": "high"}
winner = hub.allocate_task(task, "auction")
agent = coordinator.agents[winner]
result = agent.execute_task(task)
```

## Troubleshooting

### Redis Not Connected
```bash
# Check if Redis is running
redis-cli ping

# Start Redis
redis-server

# Or use Docker
docker run -d -p 6379:6379 redis
```

### Import Errors
```bash
# Install missing packages
pip install chromadb redis sentence-transformers
```

### Vector DB Errors
```python
# Check database stats
stats = vector_db.get_stats()
print(stats)

# Re-initialize if needed
vector_db = VectorDatabaseManager(db_type="chromadb")
```

## Performance Tips

1. **Use appropriate agent count**
   - Small problems: 3-5 agents
   - Large problems: 10-15 agents

2. **Choose right strategy**
   - Need speed: VOTING or SWARM
   - Need quality: DEBATE or HIERARCHICAL

3. **Batch operations**
   - Add documents in bulk
   - Use parallel agent execution

4. **Monitor system**
   ```python
   status = coordinator.get_system_status()
   health = hub.health_check()
   ```

## Resources

- **Full Guide**: `MULTIAGENT_GUIDE.md`
- **Examples**: `MULTIAGENT_EXAMPLES.md`
- **Demo**: `python demo_multiagent.py`
- **Code Style**: `AGENTS.md`

## Support

- Issues: GitHub Issues
- Docs: Project README files
- Demo: `demo_multiagent.py`
