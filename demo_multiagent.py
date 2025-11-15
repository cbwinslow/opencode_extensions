#!/usr/bin/env python3

"""
Multi-Agent Democratic Problem Solving - Comprehensive Demo
Demonstrates all features of the multi-agent system.
"""

import json
import time
from agents.multiagent_coordinator import (
    MultiAgentCoordinator,
    ProblemSolvingStrategy
)
from tools.vector_database import VectorDatabaseManager
from tools.agent_communication import AgentCommunicationHub, AgentRole


def print_section(title: str):
    """Print formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def demo_vector_database():
    """Demonstrate vector database capabilities"""
    print_section("VECTOR DATABASE DEMO")
    
    print("1. Initializing ChromaDB (FOSS vector database)...")
    vector_db = VectorDatabaseManager(db_type="chromadb")
    
    print("\n2. Adding sample documents...")
    documents = [
        {
            "content": "Multi-agent systems use distributed decision-making algorithms.",
            "metadata": {"topic": "multi-agent", "importance": "high"}
        },
        {
            "content": "Democratic voting enables consensus among autonomous agents.",
            "metadata": {"topic": "consensus", "importance": "high"}
        },
        {
            "content": "Vector databases enable semantic search over documents.",
            "metadata": {"topic": "vector-db", "importance": "medium"}
        },
        {
            "content": "Redis provides fast inter-agent communication.",
            "metadata": {"topic": "redis", "importance": "medium"}
        },
        {
            "content": "Swarm intelligence mimics collective behavior of social insects.",
            "metadata": {"topic": "swarm", "importance": "high"}
        }
    ]
    
    doc_ids = vector_db.add_documents(documents)
    print(f"   Added {len(doc_ids)} documents")
    
    print("\n3. Searching for relevant documents...")
    query = "How do agents make decisions together?"
    results = vector_db.search(query, top_k=3)
    
    print(f"\n   Query: '{query}'")
    print(f"   Found {len(results)} relevant documents:\n")
    
    for i, result in enumerate(results):
        print(f"   {i+1}. Score: {result['score']:.4f}")
        print(f"      {result['content']}")
        print(f"      Topic: {result['metadata'].get('topic', 'N/A')}\n")
    
    print("\n4. Database statistics:")
    stats = vector_db.get_stats()
    print(f"   {json.dumps(stats, indent=3)}")
    
    return vector_db


def demo_agent_communication():
    """Demonstrate agent communication system"""
    print_section("AGENT COMMUNICATION DEMO")
    
    print("1. Initializing Redis-based communication hub...")
    try:
        hub = AgentCommunicationHub()
        print("   ✓ Connected to Redis")
    except Exception as e:
        print(f"   ✗ Redis not available: {e}")
        print("   To use this feature, start Redis: redis-server")
        return None
    
    print("\n2. Registering test agents...")
    agents = [
        ("agent_alice", AgentRole.PROBLEM_SOLVER),
        ("agent_bob", AgentRole.MONITOR),
        ("agent_charlie", AgentRole.NOTE_TAKER),
    ]
    
    for agent_id, role in agents:
        hub.register_agent(agent_id, role, {"model": "test"})
        print(f"   ✓ Registered {agent_id} as {role.value}")
    
    print("\n3. Sending test messages...")
    from tools.agent_communication import MessageType
    
    msg_id = hub.send_message(
        MessageType.STATUS_UPDATE,
        "System initialized successfully",
        recipient_role=None  # Broadcast
    )
    print(f"   ✓ Sent broadcast message: {msg_id}")
    
    print("\n4. Requesting democratic vote...")
    vote_data = hub.request_vote(
        proposal="Should we optimize the algorithm?",
        options=["yes", "no", "defer"],
        timeout=5
    )
    print(f"   ✓ Vote initiated: {vote_data['vote_id']}")
    
    # Simulate votes
    hub.agent_id = "agent_alice"
    hub.cast_vote(vote_data['vote_id'], "yes")
    hub.agent_id = "agent_bob"
    hub.cast_vote(vote_data['vote_id'], "yes")
    hub.agent_id = "agent_charlie"
    hub.cast_vote(vote_data['vote_id'], "defer")
    
    time.sleep(1)
    
    print("\n5. Vote results:")
    results = hub.get_vote_results(vote_data['vote_id'])
    print(f"   Total votes: {results['total_votes']}")
    print(f"   Results: {json.dumps(results['results'], indent=3)}")
    print(f"   Winner: {results['winner']}")
    
    print("\n6. Agent status:")
    status = hub.get_agent_status()
    print(f"   Active agents: {len(status)}")
    for agent_id, info in list(status.items())[:3]:
        print(f"   - {agent_id}: {info['role']} (alive: {info['is_alive']})")
    
    print("\n7. Communication health check:")
    health = hub.health_check()
    print(f"   {json.dumps(health, indent=3)}")
    
    return hub


def demo_multiagent_solving():
    """Demonstrate multi-agent problem solving"""
    print_section("MULTI-AGENT PROBLEM SOLVING DEMO")
    
    print("1. Initializing Multi-Agent Coordinator...")
    try:
        coordinator = MultiAgentCoordinator()
        print("   ✓ Coordinator initialized")
    except Exception as e:
        print(f"   ✗ Failed to initialize: {e}")
        return None
    
    print("\n2. Spawning AI agents...")
    coordinator.spawn_agents(count=5, role_distribution={
        AgentRole.PROBLEM_SOLVER: 2,
        AgentRole.MONITOR: 1,
        AgentRole.NOTE_TAKER: 1,
        AgentRole.HEALER: 1
    })
    
    print("\n3. Testing different problem-solving strategies...\n")
    
    test_problems = [
        ("Optimize database query performance", ProblemSolvingStrategy.VOTING),
        ("Design new API endpoint", ProblemSolvingStrategy.CONSENSUS),
        ("Refactor legacy code module", ProblemSolvingStrategy.AUCTION),
        ("Implement new feature", ProblemSolvingStrategy.HIERARCHICAL),
    ]
    
    for problem, strategy in test_problems:
        print(f"\n   Problem: '{problem}'")
        print(f"   Strategy: {strategy.value}")
        print(f"   {'-'*60}")
        
        solution = coordinator.solve_problem(problem, strategy)
        
        print(f"   Solution summary:")
        for key, value in solution.items():
            if key not in ["sub_solutions", "results_count"]:
                print(f"     - {key}: {value}")
        print()
    
    print("\n4. System Status:")
    status = coordinator.get_system_status()
    print(json.dumps(status, indent=2))
    
    print("\n5. Shutting down agents...")
    coordinator.shutdown()
    
    return coordinator


def demo_integrated_workflow():
    """Demonstrate integrated workflow with all components"""
    print_section("INTEGRATED WORKFLOW DEMO")
    
    print("This demonstrates a complete workflow combining:")
    print("  • Vector database for knowledge storage")
    print("  • Redis communication for agent coordination")
    print("  • Multi-agent democratic problem solving")
    
    print("\n1. Setting up knowledge base...")
    vector_db = VectorDatabaseManager(db_type="chromadb")
    
    # Add problem-solving knowledge
    knowledge_docs = [
        {
            "content": "Algorithm optimization requires profiling and benchmarking.",
            "metadata": {"category": "optimization"}
        },
        {
            "content": "Code refactoring should maintain existing test coverage.",
            "metadata": {"category": "refactoring"}
        },
        {
            "content": "API design should follow REST principles and versioning.",
            "metadata": {"category": "api-design"}
        }
    ]
    
    vector_db.add_documents(knowledge_docs)
    print("   ✓ Knowledge base populated")
    
    print("\n2. Initializing agent network...")
    try:
        coordinator = MultiAgentCoordinator()
        coordinator.spawn_agents(count=4)
        print("   ✓ Agent network ready")
    except Exception as e:
        print(f"   ✗ Redis required for full demo: {e}")
        return
    
    print("\n3. Solving complex problem with knowledge retrieval...")
    
    # Search knowledge base
    query = "How to optimize code performance?"
    knowledge = vector_db.search(query, top_k=2)
    
    print(f"   Retrieved knowledge:")
    for k in knowledge:
        print(f"     - {k['content'][:60]}...")
    
    # Solve with agents
    problem = "Optimize critical path algorithm"
    solution = coordinator.solve_problem(
        problem,
        ProblemSolvingStrategy.HIERARCHICAL,
        context={"knowledge": knowledge}
    )
    
    print(f"\n   Solution: {solution['strategy']}")
    print(f"   Sub-problems solved: {solution['sub_problems_count']}")
    
    print("\n4. Cleanup...")
    coordinator.shutdown()
    print("   ✓ System shutdown complete")


def main():
    """Run all demonstrations"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║     MULTI-AGENT DEMOCRATIC PROBLEM SOLVING SYSTEM                   ║
║     Comprehensive Demonstration                                      ║
║                                                                      ║
║     FOSS Components:                                                 ║
║     • ChromaDB (Apache 2.0) - Vector database                       ║
║     • Redis (BSD) - Agent communication                             ║
║     • OpenRouter Free Models - AI reasoning                         ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
    """)
    
    # Run demonstrations
    demos = [
        ("Vector Database", demo_vector_database),
        ("Agent Communication", demo_agent_communication),
        ("Multi-Agent Problem Solving", demo_multiagent_solving),
        ("Integrated Workflow", demo_integrated_workflow)
    ]
    
    for name, demo_func in demos:
        try:
            demo_func()
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user")
            break
        except Exception as e:
            print(f"\n✗ Error in {name} demo: {e}")
            continue
    
    print_section("DEMO COMPLETE")
    print("""
Next steps:
  1. Install dependencies: pip install chromadb redis sentence-transformers
  2. Start Redis: redis-server
  3. Run CLI commands:
     - python cli.py vector_db init chromadb
     - python cli.py agent_comm health
     - python cli.py multiagent demo
  
For more information, see MULTIAGENT_GUIDE.md
    """)


if __name__ == "__main__":
    main()
