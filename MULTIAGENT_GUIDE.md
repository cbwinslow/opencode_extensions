# Multi-Agent Democratic Problem Solving Guide

## 🎯 Overview

This system implements **democratic, decentralized multi-agent problem solving** based on cutting-edge academic research. Multiple AI agents work together using various coordination algorithms to solve complex problems autonomously.

## 🏗️ Architecture

### Components

1. **Vector Database Layer** (`tools/vector_database.py`)
   - Document ingestion and vectorization
   - Semantic search capabilities
   - Supports: ChromaDB, Qdrant, Weaviate (all FOSS)

2. **Agent Communication Hub** (`tools/agent_communication.py`)
   - Redis-based message passing
   - Democratic voting mechanisms
   - Consensus protocols
   - Task allocation

3. **Multi-Agent Coordinator** (`agents/multiagent_coordinator.py`)
   - Agent lifecycle management
   - Problem-solving strategies
   - Algorithm implementation

### Agent Roles

- **PROBLEM_SOLVER**: Reasoning and execution
- **MONITOR**: System health monitoring
- **NOTE_TAKER**: Documentation and memory
- **HEALER**: Self-healing and recovery
- **COORDINATOR**: Task orchestration

## 📚 Academic Foundations

### Key Research Areas

1. **Decentralized Multi-Agent Reinforcement Learning (MARL)**
   - Each agent learns policies balancing individual and team objectives
   - Fully decentralized training and execution
   - Reference: "Decentralized multi-agent reinforcement learning" (Frontiers in Robotics & AI, 2024)

2. **Distributed Resource Allocation**
   - Auction-based task allocation
   - Greedy assignment algorithms
   - Negotiation protocols
   - Reference: "Survey of distributed algorithms for resource allocation" (ScienceDirect, 2024)

3. **Democratic Consensus Mechanisms**
   - Voting systems (simple majority, weighted, ranked)
   - Byzantine fault tolerance
   - Swarm intelligence patterns
   - Reference: "Swarm Intelligence Decentralized Decision Making" (IEEE, 2023)

4. **Multi-Agent Path Finding & Negotiation**
   - Automated negotiation frameworks
   - Conflict resolution strategies
   - Reference: "Decentralized multi-agent path finding framework" (Springer, 2024)

5. **LLM-Based Multi-Agent Collaboration**
   - Dynamic division of labor
   - Peer-to-peer debate
   - Cooperative reasoning
   - Reference: "Multi-Agent Collaboration Mechanisms: A Survey of LLMs" (arXiv, 2025)

## 🎮 Problem-Solving Strategies

### 1. VOTING Strategy

Democratic voting among agents to select best solution.

```python
solution = coordinator.solve_problem(
    "Optimize database queries",
    ProblemSolvingStrategy.VOTING
)
```

**Use cases:**
- Multiple solution candidates
- Quick decision needed
- Democratic fairness important

### 2. CONSENSUS Strategy

Requires agreement threshold (e.g., 66%) among agents.

```python
solution = coordinator.solve_problem(
    "Deploy to production",
    ProblemSolvingStrategy.CONSENSUS
)
```

**Use cases:**
- High-stakes decisions
- Need strong agreement
- Risk mitigation

### 3. AUCTION Strategy

Task allocated to agent with best bid (lowest cost/highest capability).

```python
solution = coordinator.solve_problem(
    "Process large dataset",
    ProblemSolvingStrategy.AUCTION
)
```

**Use cases:**
- Resource optimization
- Load balancing
- Cost minimization

### 4. SWARM Strategy

Parallel processing by multiple agents, aggregate results.

```python
solution = coordinator.solve_problem(
    "Search solution space",
    ProblemSolvingStrategy.SWARM
)
```

**Use cases:**
- Exploration problems
- Parallel computation
- Pattern recognition

### 5. DEBATE Strategy

Agents debate and refine solutions through multiple rounds.

```python
solution = coordinator.solve_problem(
    "Design system architecture",
    ProblemSolvingStrategy.DEBATE
)
```

**Use cases:**
- Complex design decisions
- Need multiple perspectives
- Refinement over time

### 6. HIERARCHICAL Strategy

Decompose problem into sub-problems, solve independently, combine.

```python
solution = coordinator.solve_problem(
    "Build complete application",
    ProblemSolvingStrategy.HIERARCHICAL
)
```

**Use cases:**
- Large complex problems
- Clear decomposition
- Divide and conquer

## 🚀 Quick Start

### Installation

```bash
# Install Python dependencies
pip install chromadb redis sentence-transformers qdrant-client weaviate-client

# Start Redis (required for agent communication)
redis-server

# Optional: Start Qdrant (alternative vector DB)
docker run -p 6333:6333 qdrant/qdrant

# Optional: Start Weaviate (alternative vector DB)
docker run -p 8080:8080 semitechnologies/weaviate
```

### Basic Usage

```python
from agents.multiagent_coordinator import MultiAgentCoordinator, ProblemSolvingStrategy

# Initialize coordinator
coordinator = MultiAgentCoordinator()

# Spawn agents
coordinator.spawn_agents(count=5)

# Solve problem
solution = coordinator.solve_problem(
    "Optimize algorithm performance",
    ProblemSolvingStrategy.VOTING
)

print(solution)
coordinator.shutdown()
```

### CLI Usage

```bash
# Run full demonstration
python demo_multiagent.py

# Or use CLI commands
python cli.py multiagent demo
python cli.py multiagent spawn 5
python cli.py multiagent solve "Optimize code" voting
python cli.py multiagent status

# Vector database operations
python cli.py vector_db init chromadb
python cli.py vector_db ingest document.txt
python cli.py vector_db search "semantic query"
python cli.py vector_db stats

# Agent communication
python cli.py agent_comm register agent1 problem_solver
python cli.py agent_comm vote "Proposal text" "yes,no,abstain"
python cli.py agent_comm status
python cli.py agent_comm health
```

## 🔧 Configuration

### Vector Database Config

```python
vector_db_config = {
    "type": "chromadb",  # or "qdrant", "weaviate"
    "persist_directory": "./vector_data",
    "collection_name": "knowledge_base",
    "embedding_model": "all-MiniLM-L6-v2"  # FOSS model
}
```

### Redis Config

```python
redis_config = {
    "host": "localhost",
    "port": 6379,
    "db": 0
}
```

### Agent Distribution

```python
role_distribution = {
    AgentRole.PROBLEM_SOLVER: 3,  # 3 problem solvers
    AgentRole.MONITOR: 1,         # 1 monitor
    AgentRole.NOTE_TAKER: 1,      # 1 note taker
    AgentRole.HEALER: 1           # 1 healer
}
```

## 🔬 Advanced Features

### Document Ingestion & Semantic Search

```python
from tools.vector_database import VectorDatabaseManager

# Initialize
vector_db = VectorDatabaseManager(db_type="chromadb")

# Ingest document
doc_ids = vector_db.ingest_file("knowledge.txt", chunk_size=500)

# Search
results = vector_db.search("How do agents coordinate?", top_k=5)

for result in results:
    print(f"Score: {result['score']}")
    print(f"Content: {result['content']}")
```

### Democratic Voting

```python
from tools.agent_communication import AgentCommunicationHub

hub = AgentCommunicationHub()

# Request vote
vote_data = hub.request_vote(
    proposal="Deploy to production?",
    options=["approve", "reject", "defer"],
    timeout=60
)

# Cast votes (from different agents)
hub.cast_vote(vote_data['vote_id'], "approve")

# Get results
results = hub.get_vote_results(vote_data['vote_id'])
print(f"Winner: {results['winner']}")
print(f"Votes: {results['results']}")
```

### Consensus Building

```python
# Request consensus with 66% agreement threshold
consensus = hub.request_consensus(
    topic="Refactor authentication module",
    required_agreement=0.66
)

# Check if consensus reached
results = hub.get_vote_results(consensus['vote_id'])
agreement = results['results'].get('agree', 0) / results['total_votes']
reached = agreement >= 0.66
```

### Task Allocation

```python
# Auction-based allocation
task = {
    "type": "data_processing",
    "priority": "high",
    "complexity": "medium"
}

winner_id = hub.allocate_task(task, allocation_method="auction")
print(f"Task allocated to: {winner_id}")
```

### Self-Healing

Agents with HEALER role automatically detect and fix issues:

```python
# Healer agents monitor system health
# When issues detected, they:
# 1. Diagnose the problem
# 2. Apply appropriate fix
# 3. Notify other agents
# 4. Log the action
```

## 🎓 Algorithms Implemented

### 1. Democratic Voting
- Simple majority
- Weighted voting
- Ranked choice
- Approval voting

### 2. Consensus Protocols
- Byzantine fault tolerance
- Raft-inspired consensus
- Threshold-based agreement

### 3. Auction Mechanisms
- First-price sealed bid
- Second-price (Vickrey)
- Combinatorial auctions

### 4. Swarm Intelligence
- Particle swarm optimization
- Ant colony optimization patterns
- Bee colony algorithms

### 5. Negotiation Protocols
- Alternating offers
- Multi-lateral negotiation
- Contract net protocol

### 6. Hierarchical Decomposition
- Problem splitting
- Sub-problem allocation
- Solution aggregation

## 🔐 FOSS Compliance

All components use Free and Open Source Software:

- **Vector Databases**: ChromaDB (Apache 2.0), Qdrant (Apache 2.0), Weaviate (BSD)
- **Communication**: Redis (BSD)
- **Embeddings**: sentence-transformers (Apache 2.0)
- **AI Models**: Via OpenRouter free tier (Mistral, LLaMA, etc.)

No proprietary services or APIs required!

## 📊 Performance Optimization

### Vector Database
```python
# Use batch operations
vector_db.add_documents(documents, embeddings=precomputed_embeddings)

# Adjust chunk size
doc_ids = vector_db.ingest_file("large.txt", chunk_size=1000, overlap=100)

# Use filters for faster search
results = vector_db.search(query, top_k=5, filters={"category": "urgent"})
```

### Agent Communication
```python
# Use message batching
for message in messages:
    hub.send_message(msg_type, content, requires_response=False)

# Subscribe patterns
hub.pubsub.psubscribe("agent:*")  # Pattern-based subscription
```

### Multi-Agent Coordination
```python
# Tune agent count based on problem complexity
coordinator.spawn_agents(count=10)  # More agents for complex problems

# Use appropriate strategy
# Simple problems -> VOTING (fast)
# Complex problems -> HIERARCHICAL or DEBATE (thorough)
```

## 🐛 Troubleshooting

### Redis Connection Issues
```bash
# Check if Redis is running
redis-cli ping

# Start Redis if not running
redis-server

# Check Redis logs
redis-cli info
```

### Vector Database Issues
```bash
# ChromaDB persistence
# Ensure write permissions to persist_directory

# Qdrant connection
curl http://localhost:6333/health

# Weaviate connection
curl http://localhost:8080/v1/.well-known/ready
```

### Agent Communication Failures
```python
# Check system health
health = hub.health_check()
print(health)

# Verify agent registration
status = hub.get_agent_status()
print(status)

# Check message log
history = hub.get_message_history(limit=10)
print(history)
```

## 📖 Additional Resources

### Academic Papers
1. "A Comprehensive Survey on Multi-Agent Cooperative Decision-Making" (arXiv:2503.13415, 2025)
2. "Multi-Agent Collaboration Mechanisms: A Survey of LLMs" (arXiv:2501.06322, 2025)
3. "Decentralized multi-agent path finding framework" (Springer, 2024)
4. "Distributed computing in multi-agent systems" (Springer, 2024)

### Tutorials
- `demo_multiagent.py` - Comprehensive demonstration
- `EXAMPLES.md` - Code examples
- `ARCHITECTURE.md` - System design details

### Community
- GitHub Issues: Report bugs and request features
- Discussions: Share use cases and ask questions
- Wiki: Community-maintained documentation

## 🤝 Contributing

Contributions welcome! Areas of interest:

1. **New Algorithms**: Implement additional multi-agent algorithms
2. **Agent Roles**: Add specialized agent types
3. **Strategies**: Create new problem-solving strategies
4. **Optimizations**: Performance improvements
5. **Documentation**: Examples and tutorials

See `CONTRIBUTING.md` for guidelines.

## 📄 License

MIT License - See LICENSE file for details.

---

**Built with 100% FOSS components for privacy, control, and freedom!**
