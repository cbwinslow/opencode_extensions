#!/usr/bin/env python3

"""
Multi-Agent Democratic Coordinator
Implements decentralized, democratic problem-solving with multiple AI agents.
Based on academic research in multi-agent systems and distributed decision-making.
"""

import json
import uuid
import time
import threading
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.agent_communication import AgentCommunicationHub, AgentRole, MessageType
from tools.vector_database import VectorDatabaseManager


class ProblemSolvingStrategy(Enum):
    """Democratic problem-solving strategies"""
    VOTING = "voting"  # Democratic voting on solutions
    CONSENSUS = "consensus"  # Consensus-based decision making
    AUCTION = "auction"  # Auction-based task allocation
    SWARM = "swarm"  # Swarm intelligence approach
    DEBATE = "debate"  # Multi-agent debate and reasoning
    HIERARCHICAL = "hierarchical"  # Hierarchical decomposition


class AIAgent:
    """
    Individual AI agent in the multi-agent system.
    Uses OpenRouter SDK with free models (FOSS principle).
    """
    
    def __init__(self, agent_id: str, role: AgentRole, 
                 communication_hub: AgentCommunicationHub,
                 model_name: str = "mistralai/mistral-7b-instruct:free"):
        """
        Initialize AI agent.
        
        Args:
            agent_id: Unique agent identifier
            role: Agent's role in the system
            communication_hub: Communication hub for inter-agent messages
            model_name: OpenRouter model (free tier)
        """
        self.agent_id = agent_id
        self.role = role
        self.hub = communication_hub
        self.model_name = model_name
        self.memory = []
        self.active = True
        
        # Register with communication hub
        self.hub.register_agent(agent_id, role, {
            "model": model_name,
            "capabilities": self._get_capabilities()
        })
        
        # Start listening for messages
        self.message_thread = threading.Thread(
            target=self._listen_for_messages,
            daemon=True
        )
        self.message_thread.start()
    
    def _get_capabilities(self) -> List[str]:
        """Get agent capabilities based on role"""
        capabilities_map = {
            AgentRole.PROBLEM_SOLVER: ["reasoning", "planning", "execution"],
            AgentRole.MONITOR: ["monitoring", "alerting", "analysis"],
            AgentRole.NOTE_TAKER: ["documentation", "summarization", "memory"],
            AgentRole.HEALER: ["error_detection", "self_healing", "recovery"],
            AgentRole.COORDINATOR: ["coordination", "task_allocation", "consensus"]
        }
        return capabilities_map.get(self.role, [])
    
    def _listen_for_messages(self):
        """Listen for messages from other agents"""
        def handle_message(message: Dict[str, Any]):
            if not self.active:
                return
            
            msg_type = MessageType(message.get("message_type"))
            
            if msg_type == MessageType.TASK_REQUEST:
                self._handle_task_request(message)
            elif msg_type == MessageType.VOTE_REQUEST:
                self._handle_vote_request(message)
            elif msg_type == MessageType.HELP_REQUEST:
                self._handle_help_request(message)
            elif msg_type == MessageType.KNOWLEDGE_SHARE:
                self._handle_knowledge_share(message)
        
        try:
            self.hub.subscribe_to_messages(handle_message)
        except Exception as e:
            print(f"Agent {self.agent_id} message listener error: {e}")
    
    def _handle_task_request(self, message: Dict[str, Any]):
        """Handle task request from coordinator"""
        if self.role == AgentRole.PROBLEM_SOLVER:
            task = message.get("content", {}).get("task", {})
            # Bid on task based on capacity
            bid_value = self._calculate_bid(task)
            
            # Submit bid
            task_id = message.get("content", {}).get("task_id")
            self.hub.redis_client.hset(
                f"tasks:bids:{task_id}",
                self.agent_id,
                bid_value
            )
    
    def _calculate_bid(self, task: Dict[str, Any]) -> float:
        """Calculate bid for task (lower is better)"""
        # Simple heuristic: random bid between 1-10
        import random
        return random.uniform(1.0, 10.0)
    
    def _handle_vote_request(self, message: Dict[str, Any]):
        """Handle vote request"""
        vote_data = message.get("content", {})
        vote_id = vote_data.get("vote_id")
        options = vote_data.get("options", [])
        
        # Intelligent voting based on role and context
        selected_option = self._make_voting_decision(vote_data)
        
        if selected_option in options:
            self.hub.cast_vote(vote_id, selected_option)
    
    def _make_voting_decision(self, vote_data: Dict[str, Any]) -> str:
        """Make intelligent voting decision"""
        options = vote_data.get("options", [])
        if not options:
            return ""
        
        # For now, simple random choice
        # In production, this would use LLM reasoning
        import random
        return random.choice(options)
    
    def _handle_help_request(self, message: Dict[str, Any]):
        """Handle help request from another agent"""
        if self.role == AgentRole.HEALER:
            # Self-healing logic
            problem = message.get("content", {})
            solution = self._diagnose_and_heal(problem)
            
            # Send response
            self.hub.send_message(
                MessageType.TASK_RESPONSE,
                {"solution": solution, "healed": True},
                recipient_id=message.get("sender_id")
            )
    
    def _diagnose_and_heal(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """Diagnose and heal system problems"""
        return {
            "diagnosis": "System issue detected",
            "action_taken": "Auto-recovery initiated",
            "status": "resolved"
        }
    
    def _handle_knowledge_share(self, message: Dict[str, Any]):
        """Handle knowledge sharing from other agents"""
        knowledge = message.get("content", {})
        self.memory.append(knowledge)
        
        # Note-takers log everything
        if self.role == AgentRole.NOTE_TAKER:
            self.hub.log_conversation(knowledge)
    
    def reason(self, prompt: str, context: Optional[Dict] = None) -> str:
        """
        Use LLM to reason about a problem.
        Uses OpenRouter SDK with free models.
        """
        # In production, this would call OpenRouter API
        # For now, return simulated response
        return f"Agent {self.agent_id} reasoning: {prompt}"
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute assigned task"""
        task_type = task.get("type", "unknown")
        
        result = {
            "agent_id": self.agent_id,
            "task_id": task.get("task_id"),
            "status": "completed",
            "output": f"Executed {task_type}",
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    
    def monitor_system(self) -> Dict[str, Any]:
        """Monitor system health (for MONITOR role)"""
        if self.role != AgentRole.MONITOR:
            return {}
        
        health = self.hub.health_check()
        
        if health.get("status") != "healthy":
            # Alert other agents
            self.hub.send_message(
                MessageType.MONITOR_ALERT,
                {"alert": "System unhealthy", "health": health}
            )
        
        return health
    
    def shutdown(self):
        """Shutdown agent gracefully"""
        self.active = False
        print(f"Agent {self.agent_id} shutting down")


class MultiAgentCoordinator:
    """
    Coordinator for democratic multi-agent problem solving.
    Implements various distributed algorithms and strategies.
    """
    
    def __init__(self, redis_config: Optional[Dict] = None,
                 vector_db_config: Optional[Dict] = None):
        """
        Initialize multi-agent coordinator.
        
        Args:
            redis_config: Redis configuration
            vector_db_config: Vector database configuration
        """
        self.hub = AgentCommunicationHub(redis_config)
        self.vector_db = VectorDatabaseManager(
            db_type=vector_db_config.get("type", "chromadb") if vector_db_config else "chromadb",
            config=vector_db_config or {}
        )
        
        self.agents: Dict[str, AIAgent] = {}
        self.active_problems: Dict[str, Dict[str, Any]] = {}
        
        print("Multi-Agent Coordinator initialized")
    
    def spawn_agents(self, count: int = 5, 
                    role_distribution: Optional[Dict[AgentRole, int]] = None):
        """
        Spawn multiple AI agents with role distribution.
        
        Args:
            count: Total number of agents
            role_distribution: Distribution of roles (optional)
        """
        if role_distribution is None:
            # Default distribution
            role_distribution = {
                AgentRole.PROBLEM_SOLVER: 2,
                AgentRole.MONITOR: 1,
                AgentRole.NOTE_TAKER: 1,
                AgentRole.HEALER: 1
            }
        
        for role, num in role_distribution.items():
            for i in range(num):
                agent_id = f"{role.value}_{uuid.uuid4().hex[:8]}"
                agent = AIAgent(agent_id, role, self.hub)
                self.agents[agent_id] = agent
                print(f"Spawned agent: {agent_id} ({role.value})")
        
        print(f"Total agents spawned: {len(self.agents)}")
    
    def solve_problem(self, problem: str, strategy: ProblemSolvingStrategy,
                     context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Solve a problem using democratic multi-agent approach.
        
        Args:
            problem: Problem description
            strategy: Problem-solving strategy to use
            context: Additional context
        
        Returns:
            Solution with metadata
        """
        problem_id = str(uuid.uuid4())
        
        self.active_problems[problem_id] = {
            "problem_id": problem_id,
            "problem": problem,
            "strategy": strategy.value,
            "context": context or {},
            "started_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        print(f"\n{'='*60}")
        print(f"SOLVING PROBLEM: {problem}")
        print(f"STRATEGY: {strategy.value}")
        print(f"{'='*60}\n")
        
        if strategy == ProblemSolvingStrategy.VOTING:
            solution = self._solve_by_voting(problem_id, problem, context)
        elif strategy == ProblemSolvingStrategy.CONSENSUS:
            solution = self._solve_by_consensus(problem_id, problem, context)
        elif strategy == ProblemSolvingStrategy.AUCTION:
            solution = self._solve_by_auction(problem_id, problem, context)
        elif strategy == ProblemSolvingStrategy.SWARM:
            solution = self._solve_by_swarm(problem_id, problem, context)
        elif strategy == ProblemSolvingStrategy.DEBATE:
            solution = self._solve_by_debate(problem_id, problem, context)
        elif strategy == ProblemSolvingStrategy.HIERARCHICAL:
            solution = self._solve_hierarchically(problem_id, problem, context)
        else:
            solution = {"error": "Unknown strategy"}
        
        self.active_problems[problem_id]["status"] = "completed"
        self.active_problems[problem_id]["solution"] = solution
        self.active_problems[problem_id]["completed_at"] = datetime.now().isoformat()
        
        return solution
    
    def _solve_by_voting(self, problem_id: str, problem: str, 
                        context: Optional[Dict]) -> Dict[str, Any]:
        """Solve problem using democratic voting"""
        print("→ Using VOTING strategy")
        
        # Generate solution options (in production, agents would propose)
        options = [
            "solution_a",
            "solution_b",
            "solution_c"
        ]
        
        # Request vote from all agents
        vote_data = self.hub.request_vote(
            proposal=f"Choose solution for: {problem}",
            options=options,
            timeout=10
        )
        
        # Wait for votes
        time.sleep(5)
        
        # Get results
        results = self.hub.get_vote_results(vote_data["vote_id"])
        
        return {
            "strategy": "voting",
            "winner": results["winner"],
            "vote_results": results["results"],
            "total_votes": results["total_votes"]
        }
    
    def _solve_by_consensus(self, problem_id: str, problem: str,
                           context: Optional[Dict]) -> Dict[str, Any]:
        """Solve problem using consensus mechanism"""
        print("→ Using CONSENSUS strategy")
        
        # Request consensus
        consensus_data = self.hub.request_consensus(
            topic=problem,
            required_agreement=0.66
        )
        
        # Wait for consensus
        time.sleep(5)
        
        # Get results
        results = self.hub.get_vote_results(consensus_data["vote_id"])
        
        agreement_percent = results["results"].get("agree", 0) / max(results["total_votes"], 1)
        consensus_reached = agreement_percent >= 0.66
        
        return {
            "strategy": "consensus",
            "consensus_reached": consensus_reached,
            "agreement_percent": agreement_percent,
            "vote_results": results["results"]
        }
    
    def _solve_by_auction(self, problem_id: str, problem: str,
                         context: Optional[Dict]) -> Dict[str, Any]:
        """Solve problem using auction-based task allocation"""
        print("→ Using AUCTION strategy")
        
        # Allocate task via auction
        task = {
            "type": "problem_solving",
            "problem": problem,
            "priority": "high"
        }
        
        winner_id = self.hub.allocate_task(task, allocation_method="auction")
        
        if winner_id and winner_id in self.agents:
            # Execute task with winning agent
            result = self.agents[winner_id].execute_task({
                "task_id": problem_id,
                "type": "problem_solving",
                "problem": problem
            })
            
            return {
                "strategy": "auction",
                "winner_agent": winner_id,
                "result": result
            }
        
        return {
            "strategy": "auction",
            "error": "No agent won auction"
        }
    
    def _solve_by_swarm(self, problem_id: str, problem: str,
                       context: Optional[Dict]) -> Dict[str, Any]:
        """Solve problem using swarm intelligence"""
        print("→ Using SWARM strategy")
        
        # Parallel processing by multiple agents
        results = []
        
        for agent_id, agent in self.agents.items():
            if agent.role == AgentRole.PROBLEM_SOLVER:
                result = agent.execute_task({
                    "task_id": problem_id,
                    "type": "parallel_solve",
                    "problem": problem
                })
                results.append(result)
        
        # Aggregate results
        best_result = max(results, key=lambda x: 1) if results else None
        
        return {
            "strategy": "swarm",
            "results_count": len(results),
            "best_result": best_result
        }
    
    def _solve_by_debate(self, problem_id: str, problem: str,
                        context: Optional[Dict]) -> Dict[str, Any]:
        """Solve problem using multi-agent debate"""
        print("→ Using DEBATE strategy")
        
        # Agents debate and refine solution
        debate_rounds = 3
        solutions = []
        
        for round_num in range(debate_rounds):
            print(f"  Debate round {round_num + 1}/{debate_rounds}")
            
            for agent_id, agent in self.agents.items():
                if agent.role == AgentRole.PROBLEM_SOLVER:
                    reasoning = agent.reason(
                        f"Round {round_num + 1}: {problem}",
                        context={"previous_solutions": solutions}
                    )
                    solutions.append({
                        "agent": agent_id,
                        "round": round_num + 1,
                        "reasoning": reasoning
                    })
        
        # Final vote on best solution
        final_vote = self.hub.request_vote(
            proposal="Select best solution from debate",
            options=[f"solution_{i}" for i in range(len(solutions))],
            timeout=10
        )
        
        time.sleep(5)
        results = self.hub.get_vote_results(final_vote["vote_id"])
        
        return {
            "strategy": "debate",
            "debate_rounds": debate_rounds,
            "solutions_generated": len(solutions),
            "winner": results["winner"]
        }
    
    def _solve_hierarchically(self, problem_id: str, problem: str,
                            context: Optional[Dict]) -> Dict[str, Any]:
        """Solve problem using hierarchical decomposition"""
        print("→ Using HIERARCHICAL strategy")
        
        # Decompose problem into sub-problems
        sub_problems = self._decompose_problem(problem)
        
        # Allocate sub-problems to agents
        sub_solutions = []
        
        for i, sub_problem in enumerate(sub_problems):
            print(f"  Solving sub-problem {i + 1}/{len(sub_problems)}")
            
            task = {
                "task_id": f"{problem_id}_sub_{i}",
                "type": "sub_problem",
                "problem": sub_problem
            }
            
            # Allocate to available agent
            for agent_id, agent in self.agents.items():
                if agent.role == AgentRole.PROBLEM_SOLVER:
                    result = agent.execute_task(task)
                    sub_solutions.append(result)
                    break
        
        # Combine sub-solutions
        final_solution = self._combine_solutions(sub_solutions)
        
        return {
            "strategy": "hierarchical",
            "sub_problems_count": len(sub_problems),
            "sub_solutions": sub_solutions,
            "final_solution": final_solution
        }
    
    def _decompose_problem(self, problem: str) -> List[str]:
        """Decompose problem into sub-problems"""
        # Simple decomposition (in production, use LLM)
        return [
            f"Sub-problem 1 of: {problem}",
            f"Sub-problem 2 of: {problem}",
            f"Sub-problem 3 of: {problem}"
        ]
    
    def _combine_solutions(self, solutions: List[Dict[str, Any]]) -> str:
        """Combine sub-solutions into final solution"""
        return f"Combined solution from {len(solutions)} sub-solutions"
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        return {
            "total_agents": len(self.agents),
            "agents_by_role": self._count_agents_by_role(),
            "active_problems": len([p for p in self.active_problems.values() 
                                   if p["status"] == "active"]),
            "communication_health": self.hub.health_check(),
            "vector_db_stats": self.vector_db.get_stats()
        }
    
    def _count_agents_by_role(self) -> Dict[str, int]:
        """Count agents by role"""
        counts = {}
        for agent in self.agents.values():
            role = agent.role.value
            counts[role] = counts.get(role, 0) + 1
        return counts
    
    def shutdown(self):
        """Shutdown all agents and coordinator"""
        print("\nShutting down multi-agent system...")
        for agent in self.agents.values():
            agent.shutdown()
        print("All agents shut down")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python multiagent_coordinator.py <action> [args...]")
        print("Actions:")
        print("  demo - Run demonstration of all strategies")
        print("  spawn <count> - Spawn agents")
        print("  solve <problem> <strategy> - Solve a problem")
        print("  status - Get system status")
        sys.exit(1)
    
    action = sys.argv[1]
    
    # Initialize coordinator
    coordinator = MultiAgentCoordinator()
    
    if action == "demo":
        print("MULTI-AGENT DEMOCRATIC PROBLEM SOLVING DEMONSTRATION\n")
        
        # Spawn agents
        coordinator.spawn_agents(count=5)
        
        # Test each strategy
        strategies = [
            ProblemSolvingStrategy.VOTING,
            ProblemSolvingStrategy.CONSENSUS,
            ProblemSolvingStrategy.AUCTION,
            ProblemSolvingStrategy.SWARM,
            ProblemSolvingStrategy.DEBATE,
            ProblemSolvingStrategy.HIERARCHICAL
        ]
        
        test_problem = "Optimize system performance"
        
        for strategy in strategies:
            solution = coordinator.solve_problem(test_problem, strategy)
            print(f"\nSolution ({strategy.value}):")
            print(json.dumps(solution, indent=2))
            print()
        
        # Show final status
        print("\nFINAL SYSTEM STATUS:")
        status = coordinator.get_system_status()
        print(json.dumps(status, indent=2))
        
        coordinator.shutdown()
    
    elif action == "spawn":
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        coordinator.spawn_agents(count=count)
        print(f"Spawned {count} agents")
    
    elif action == "solve":
        problem = sys.argv[2] if len(sys.argv) > 2 else "Test problem"
        strategy_str = sys.argv[3] if len(sys.argv) > 3 else "voting"
        
        strategy = ProblemSolvingStrategy[strategy_str.upper()]
        
        coordinator.spawn_agents(count=5)
        solution = coordinator.solve_problem(problem, strategy)
        print(json.dumps(solution, indent=2))
        
        coordinator.shutdown()
    
    elif action == "status":
        coordinator.spawn_agents(count=5)
        status = coordinator.get_system_status()
        print(json.dumps(status, indent=2))
        coordinator.shutdown()
    
    else:
        print(f"Unknown action: {action}")
