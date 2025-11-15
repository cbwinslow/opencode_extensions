#!/usr/bin/env python3

"""
Research Assistant for Multi-Agent Systems
Helps agents access and synthesize academic research papers.
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime


class AcademicResearchAssistant:
    """
    Assistant for accessing academic research on multi-agent systems.
    Provides summaries of key papers and algorithms.
    """
    
    # Academic papers on multi-agent democratic problem solving (2024-2025)
    RESEARCH_DATABASE = {
        "multi_agent_decision_making": {
            "title": "A Comprehensive Survey on Multi-Agent Cooperative Decision-Making",
            "authors": ["Multiple Authors"],
            "year": 2025,
            "arxiv": "2503.13415",
            "url": "https://arxiv.org/abs/2503.13415",
            "summary": "Comprehensive survey covering major algorithms, simulation platforms, and problem-solving scenarios in multi-agent systems. Organizes approaches into rule-based, game theory, evolutionary algorithms, MARL, and LLM reasoning.",
            "key_concepts": [
                "Multi-Agent Reinforcement Learning (MARL)",
                "Game theory for incentive design",
                "Evolutionary algorithms",
                "LLM-based reasoning",
                "Cooperative decision-making"
            ],
            "algorithms": [
                "Actor-critic frameworks",
                "Distributed Q-learning",
                "Policy gradient methods"
            ]
        },
        "llm_collaboration": {
            "title": "Multi-Agent Collaboration Mechanisms: A Survey of LLMs",
            "authors": ["Multiple Authors"],
            "year": 2025,
            "arxiv": "2501.06322",
            "url": "https://arxiv.org/abs/2501.06322",
            "summary": "Research on collaborative agentic AI powered by LLMs. Covers dynamic division of labor, peer-to-peer debate, and cooperative reasoning among distributed agents.",
            "key_concepts": [
                "LLM-powered agents",
                "Dynamic division of labor",
                "Peer-to-peer debate",
                "Cooperative reasoning",
                "Democratic agent interactions"
            ],
            "algorithms": [
                "Debate-based refinement",
                "Collaborative prompting",
                "Multi-agent conversation"
            ]
        },
        "decentralized_marl": {
            "title": "Decentralized Multi-Agent Reinforcement Learning",
            "authors": ["Frontiers in Robotics & AI"],
            "year": 2024,
            "url": "https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2024.1229026",
            "summary": "Modern actor-critic frameworks for decentralized training and execution. Agents model others as responsive entities, balancing individual rewards with team objectives.",
            "key_concepts": [
                "Decentralized training",
                "Actor-critic methods",
                "Privacy-preserving learning",
                "Scalable coordination"
            ],
            "algorithms": [
                "Decentralized actor-critic",
                "Independent learners",
                "Value decomposition networks"
            ]
        },
        "resource_allocation": {
            "title": "Survey of Distributed Algorithms for Resource Allocation",
            "authors": ["ScienceDirect"],
            "year": 2024,
            "url": "https://www.sciencedirect.com/science/article/pii/S1367578824000518",
            "summary": "Distributed algorithms for resource allocation and consensus. Includes auction-based methods, greedy assignments, and negotiation protocols for agents to allocate tasks without global information.",
            "key_concepts": [
                "Auction-based allocation",
                "Greedy assignment",
                "Negotiation protocols",
                "Distributed consensus"
            ],
            "algorithms": [
                "First-price sealed bid auction",
                "Vickrey auction",
                "Combinatorial auctions",
                "Contract net protocol"
            ]
        },
        "path_finding_negotiation": {
            "title": "Decentralized Multi-Agent Path Finding Framework",
            "authors": ["Springer"],
            "year": 2024,
            "url": "https://link.springer.com/article/10.1007/s10458-024-09639-8",
            "summary": "Framework for automated negotiation in multi-agent systems. Focuses on conflict resolution and coordination without centralized control.",
            "key_concepts": [
                "Automated negotiation",
                "Conflict resolution",
                "Decentralized coordination",
                "Path finding algorithms"
            ],
            "algorithms": [
                "Alternating offers",
                "Multi-lateral negotiation",
                "Best-response dynamics"
            ]
        },
        "swarm_intelligence": {
            "title": "Swarm Intelligence Decentralized Decision Making",
            "authors": ["IEEE"],
            "year": 2023,
            "url": "https://ieeexplore.ieee.org/document/10192625",
            "summary": "Democratic systems that avoid centralized control through swarm intelligence. Includes voting, distributed negotiation, and best-response dynamics.",
            "key_concepts": [
                "Swarm intelligence",
                "Collective behavior",
                "Distributed voting",
                "Emergent coordination"
            ],
            "algorithms": [
                "Particle swarm optimization",
                "Ant colony optimization",
                "Bee colony algorithms",
                "Flocking behaviors"
            ]
        },
        "distributed_computing": {
            "title": "Distributed Computing in Multi-Agent Systems",
            "authors": ["Springer"],
            "year": 2024,
            "url": "https://link.springer.com/content/pdf/10.1007/s00607-024-01356-0.pdf",
            "summary": "Privacy-preserving distributed machine learning. Algorithms maintain data confidentiality by splitting learning tasks among agents, essential for democratic distributed systems.",
            "key_concepts": [
                "Distributed machine learning",
                "Privacy preservation",
                "Federated learning",
                "Data sovereignty"
            ],
            "algorithms": [
                "Federated averaging",
                "Split learning",
                "Differential privacy"
            ]
        }
    }
    
    def __init__(self):
        """Initialize research assistant"""
        self.database = self.RESEARCH_DATABASE
    
    def search_papers(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant papers based on query.
        
        Args:
            query: Search query
            max_results: Maximum results to return
        
        Returns:
            List of matching papers
        """
        query_lower = query.lower()
        results = []
        
        for paper_id, paper in self.database.items():
            score = 0
            
            # Check title
            if any(word in paper["title"].lower() for word in query_lower.split()):
                score += 3
            
            # Check summary
            if any(word in paper["summary"].lower() for word in query_lower.split()):
                score += 2
            
            # Check key concepts
            for concept in paper["key_concepts"]:
                if any(word in concept.lower() for word in query_lower.split()):
                    score += 2
            
            # Check algorithms
            for algo in paper["algorithms"]:
                if any(word in algo.lower() for word in query_lower.split()):
                    score += 1
            
            if score > 0:
                results.append({
                    "id": paper_id,
                    "score": score,
                    **paper
                })
        
        # Sort by score
        results.sort(key=lambda x: x["score"], reverse=True)
        
        return results[:max_results]
    
    def get_paper(self, paper_id: str) -> Optional[Dict[str, Any]]:
        """
        Get details of a specific paper.
        
        Args:
            paper_id: Paper identifier
        
        Returns:
            Paper details or None
        """
        return self.database.get(paper_id)
    
    def get_algorithms(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get list of algorithms from papers.
        
        Args:
            category: Optional category filter
        
        Returns:
            List of algorithms with sources
        """
        algorithms = []
        
        for paper_id, paper in self.database.items():
            if category and category.lower() not in paper_id.lower():
                continue
            
            for algo in paper["algorithms"]:
                algorithms.append({
                    "algorithm": algo,
                    "source_paper": paper["title"],
                    "year": paper["year"],
                    "paper_id": paper_id
                })
        
        return algorithms
    
    def get_implementation_guide(self, algorithm_name: str) -> Dict[str, Any]:
        """
        Get implementation guidance for an algorithm.
        
        Args:
            algorithm_name: Name of algorithm
        
        Returns:
            Implementation guide
        """
        # Search for papers mentioning this algorithm
        papers = []
        for paper_id, paper in self.database.items():
            if any(algorithm_name.lower() in algo.lower() for algo in paper["algorithms"]):
                papers.append(paper)
        
        if not papers:
            return {
                "algorithm": algorithm_name,
                "status": "not_found",
                "message": "No papers found for this algorithm"
            }
        
        return {
            "algorithm": algorithm_name,
            "status": "found",
            "papers": papers,
            "implementation_notes": self._get_implementation_notes(algorithm_name),
            "code_example": self._get_code_example(algorithm_name)
        }
    
    def _get_implementation_notes(self, algorithm_name: str) -> str:
        """Get implementation notes for algorithm"""
        notes = {
            "auction": "Implement sealed-bid or open auction. Agents bid based on cost/capability. Winner selected by lowest cost or highest value.",
            "voting": "Each agent casts vote. Count votes and determine winner by majority, plurality, or threshold. Support weighted voting if needed.",
            "consensus": "Request agreement from all agents. Require threshold (e.g., 66%) to reach consensus. Use timeout for non-responsive agents.",
            "swarm": "Multiple agents work in parallel. Each explores solution space independently. Aggregate results to find best solution.",
            "debate": "Agents propose solutions and critique each other. Multiple rounds of refinement. Final vote on best solution.",
            "hierarchical": "Decompose problem into sub-problems. Allocate sub-problems to agents. Combine solutions bottom-up."
        }
        
        for key, note in notes.items():
            if key in algorithm_name.lower():
                return note
        
        return "General implementation: Design agent coordination protocol, define message types, implement decision logic."
    
    def _get_code_example(self, algorithm_name: str) -> str:
        """Get code example for algorithm"""
        if "auction" in algorithm_name.lower():
            return """
# Auction-based task allocation
def allocate_via_auction(task, agents):
    bids = {}
    for agent in agents:
        bids[agent.id] = agent.calculate_bid(task)
    
    winner = min(bids.items(), key=lambda x: x[1])[0]
    return winner
            """
        elif "voting" in algorithm_name.lower():
            return """
# Democratic voting
def vote_on_solution(solutions, agents):
    votes = {}
    for solution in solutions:
        votes[solution] = 0
    
    for agent in agents:
        choice = agent.vote(solutions)
        votes[choice] += 1
    
    winner = max(votes.items(), key=lambda x: x[1])[0]
    return winner
            """
        elif "consensus" in algorithm_name.lower():
            return """
# Consensus building
def reach_consensus(proposal, agents, threshold=0.66):
    agreements = 0
    for agent in agents:
        if agent.evaluate(proposal):
            agreements += 1
    
    agreement_rate = agreements / len(agents)
    return agreement_rate >= threshold
            """
        
        return "# Code example not available for this algorithm"
    
    def summarize_research(self, topic: str) -> str:
        """
        Generate research summary on a topic.
        
        Args:
            topic: Research topic
        
        Returns:
            Summary text
        """
        papers = self.search_papers(topic, max_results=10)
        
        if not papers:
            return f"No research found on topic: {topic}"
        
        summary = f"Research Summary: {topic}\n"
        summary += "=" * 60 + "\n\n"
        
        for i, paper in enumerate(papers[:5]):
            summary += f"{i+1}. {paper['title']} ({paper['year']})\n"
            summary += f"   {paper['summary'][:200]}...\n"
            summary += f"   Key concepts: {', '.join(paper['key_concepts'][:3])}\n\n"
        
        # Extract common themes
        all_concepts = []
        for paper in papers:
            all_concepts.extend(paper['key_concepts'])
        
        concept_counts = {}
        for concept in all_concepts:
            concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        common_concepts = sorted(concept_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        summary += "\nCommon Themes:\n"
        for concept, count in common_concepts:
            summary += f"  • {concept} (mentioned in {count} papers)\n"
        
        return summary
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get research database statistics"""
        total_papers = len(self.database)
        total_algorithms = sum(len(p["algorithms"]) for p in self.database.values())
        years = [p["year"] for p in self.database.values()]
        
        return {
            "total_papers": total_papers,
            "total_algorithms": total_algorithms,
            "year_range": f"{min(years)}-{max(years)}",
            "categories": list(self.database.keys())
        }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python research_assistant.py <action> [args...]")
        print("Actions:")
        print("  search <query> - Search for papers")
        print("  get <paper_id> - Get paper details")
        print("  algorithms [category] - List algorithms")
        print("  guide <algorithm> - Get implementation guide")
        print("  summarize <topic> - Summarize research on topic")
        print("  stats - Get database statistics")
        sys.exit(1)
    
    action = sys.argv[1]
    assistant = AcademicResearchAssistant()
    
    if action == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else "multi-agent"
        results = assistant.search_papers(query)
        
        print(f"Search results for: {query}\n")
        for i, paper in enumerate(results):
            print(f"{i+1}. {paper['title']} ({paper['year']})")
            print(f"   Score: {paper['score']}")
            print(f"   {paper['summary'][:150]}...")
            print(f"   URL: {paper['url']}\n")
    
    elif action == "get":
        paper_id = sys.argv[2] if len(sys.argv) > 2 else "multi_agent_decision_making"
        paper = assistant.get_paper(paper_id)
        
        if paper:
            print(json.dumps(paper, indent=2))
        else:
            print(f"Paper not found: {paper_id}")
    
    elif action == "algorithms":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        algorithms = assistant.get_algorithms(category)
        
        print(f"Algorithms{' in ' + category if category else ''}:\n")
        for algo in algorithms:
            print(f"• {algo['algorithm']}")
            print(f"  Source: {algo['source_paper']} ({algo['year']})\n")
    
    elif action == "guide":
        algorithm = sys.argv[2] if len(sys.argv) > 2 else "voting"
        guide = assistant.get_implementation_guide(algorithm)
        
        print(json.dumps(guide, indent=2))
    
    elif action == "summarize":
        topic = sys.argv[2] if len(sys.argv) > 2 else "multi-agent systems"
        summary = assistant.summarize_research(topic)
        print(summary)
    
    elif action == "stats":
        stats = assistant.get_statistics()
        print(json.dumps(stats, indent=2))
    
    else:
        print(f"Unknown action: {action}")
