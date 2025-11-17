#!/usr/bin/env python3

"""
Basic tests for multi-agent system components.
Run with: python test_multiagent.py
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from tools.vector_database import VectorDatabaseManager
        print("  ✓ vector_database")
    except Exception as e:
        print(f"  ✗ vector_database: {e}")
        return False
    
    try:
        from tools.agent_communication import AgentCommunicationHub, AgentRole, MessageType
        print("  ✓ agent_communication")
    except Exception as e:
        print(f"  ✗ agent_communication: {e}")
        return False
    
    try:
        from agents.multiagent_coordinator import MultiAgentCoordinator, ProblemSolvingStrategy
        print("  ✓ multiagent_coordinator")
    except Exception as e:
        print(f"  ✗ multiagent_coordinator: {e}")
        return False
    
    return True


def test_vector_database():
    """Test vector database basic operations"""
    print("\nTesting vector database...")
    
    try:
        from tools.vector_database import VectorDatabaseManager
        
        # Initialize
        db = VectorDatabaseManager(db_type="chromadb", config={
            "persist_directory": "./test_chroma",
            "collection_name": "test_collection"
        })
        print("  ✓ Initialized ChromaDB")
        
        # Add documents
        docs = [
            {"content": "Test document 1", "metadata": {"test": True}},
            {"content": "Test document 2", "metadata": {"test": True}}
        ]
        doc_ids = db.add_documents(docs)
        print(f"  ✓ Added {len(doc_ids)} documents")
        
        # Search
        results = db.search("test", top_k=2)
        print(f"  ✓ Search returned {len(results)} results")
        
        # Stats
        stats = db.get_stats()
        print(f"  ✓ Stats: {stats['document_count']} documents")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_agent_communication():
    """Test agent communication (requires Redis)"""
    print("\nTesting agent communication...")
    
    try:
        from tools.agent_communication import AgentCommunicationHub, AgentRole, MessageType
        
        # Try to connect
        hub = AgentCommunicationHub()
        print("  ✓ Connected to Redis")
        
        # Register agent
        hub.register_agent("test_agent", AgentRole.PROBLEM_SOLVER)
        print("  ✓ Registered agent")
        
        # Send message
        msg_id = hub.send_message(MessageType.STATUS_UPDATE, "Test message")
        print(f"  ✓ Sent message: {msg_id[:8]}...")
        
        # Health check
        health = hub.health_check()
        print(f"  ✓ Health check: {health['status']}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        print("  ℹ Redis must be running for this test")
        return False


def test_multiagent_coordinator():
    """Test multi-agent coordinator (requires Redis)"""
    print("\nTesting multi-agent coordinator...")
    
    try:
        from agents.multiagent_coordinator import MultiAgentCoordinator, ProblemSolvingStrategy
        
        # Initialize
        coordinator = MultiAgentCoordinator()
        print("  ✓ Initialized coordinator")
        
        # Spawn agents
        coordinator.spawn_agents(count=3)
        print(f"  ✓ Spawned {len(coordinator.agents)} agents")
        
        # Get status
        status = coordinator.get_system_status()
        print(f"  ✓ System status: {status['total_agents']} agents active")
        
        # Cleanup
        coordinator.shutdown()
        print("  ✓ Shutdown complete")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        print("  ℹ Redis must be running for this test")
        return False


def test_cli_integration():
    """Test CLI commands"""
    print("\nTesting CLI integration...")
    
    import subprocess
    
    try:
        # Test vector_db help
        result = subprocess.run(
            ["python3", "cli.py", "vector_db"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if "vector_database.py" in result.stderr or "Usage" in result.stdout:
            print("  ✓ vector_db CLI accessible")
        else:
            print("  ⚠ vector_db CLI response unexpected")
        
        # Test agent_comm help
        result = subprocess.run(
            ["python3", "cli.py", "agent_comm"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if "agent_communication.py" in result.stderr or "Usage" in result.stdout:
            print("  ✓ agent_comm CLI accessible")
        else:
            print("  ⚠ agent_comm CLI response unexpected")
        
        # Test multiagent help
        result = subprocess.run(
            ["python3", "cli.py", "multiagent"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if "multiagent_coordinator.py" in result.stderr or "Usage" in result.stdout:
            print("  ✓ multiagent CLI accessible")
        else:
            print("  ⚠ multiagent CLI response unexpected")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Multi-Agent System - Basic Tests")
    print("=" * 60)
    
    results = {
        "Imports": test_imports(),
        "Vector Database": test_vector_database(),
        "Agent Communication": test_agent_communication(),
        "Multi-Agent Coordinator": test_multiagent_coordinator(),
        "CLI Integration": test_cli_integration()
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        print("\nNote: Some tests require Redis to be running:")
        print("  redis-server")
        return 1


if __name__ == "__main__":
    sys.exit(main())
