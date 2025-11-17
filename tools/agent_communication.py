#!/usr/bin/env python3

"""
Redis-based Agent Communication System for Multi-Agent Coordination.
Enables democratic, decentralized communication between AI agents.
"""

import json
import time
import uuid
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime
from enum import Enum

class MessageType(Enum):
    """Types of inter-agent messages"""
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    VOTE_REQUEST = "vote_request"
    VOTE_CAST = "vote_cast"
    CONSENSUS_REACHED = "consensus_reached"
    STATUS_UPDATE = "status_update"
    KNOWLEDGE_SHARE = "knowledge_share"
    HELP_REQUEST = "help_request"
    SELF_HEAL = "self_heal"
    MONITOR_ALERT = "monitor_alert"
    NOTE_TAKING = "note_taking"


class AgentRole(Enum):
    """Agent roles in the democratic system"""
    PROBLEM_SOLVER = "problem_solver"
    MONITOR = "monitor"
    NOTE_TAKER = "note_taker"
    HEALER = "healer"
    COORDINATOR = "coordinator"
    VOTER = "voter"


class AgentCommunicationHub:
    """
    Redis-based communication hub for multi-agent systems.
    Implements democratic coordination patterns.
    """
    
    def __init__(self, redis_config: Optional[Dict] = None):
        """
        Initialize agent communication hub.
        
        Args:
            redis_config: Redis connection configuration
        """
        self.redis_config = redis_config or {
            "host": "localhost",
            "port": 6379,
            "db": 0
        }
        self.redis_client = None
        self.pubsub = None
        self.agent_id = str(uuid.uuid4())
        self.agent_role = AgentRole.PROBLEM_SOLVER
        
        self._connect_redis()
    
    def _connect_redis(self):
        """Connect to Redis server"""
        try:
            import redis
            
            self.redis_client = redis.Redis(
                host=self.redis_config.get("host", "localhost"),
                port=self.redis_config.get("port", 6379),
                db=self.redis_config.get("db", 0),
                decode_responses=True
            )
            
            # Test connection
            self.redis_client.ping()
            print(f"Connected to Redis at {self.redis_config['host']}:{self.redis_config['port']}")
            
            # Initialize pubsub
            self.pubsub = self.redis_client.pubsub()
            
        except ImportError:
            print("Redis not installed. Install with: pip install redis")
            raise
        except Exception as e:
            print(f"Failed to connect to Redis: {e}")
            print("Make sure Redis server is running: redis-server")
            raise
    
    def register_agent(self, agent_id: str, role: AgentRole, 
                      metadata: Optional[Dict] = None) -> bool:
        """
        Register an agent in the system.
        
        Args:
            agent_id: Unique agent identifier
            role: Agent's role in the system
            metadata: Additional agent metadata
        
        Returns:
            Success status
        """
        self.agent_id = agent_id
        self.agent_role = role
        
        agent_data = {
            "agent_id": agent_id,
            "role": role.value,
            "status": "active",
            "registered_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        # Store agent in registry
        self.redis_client.hset(
            "agents:registry",
            agent_id,
            json.dumps(agent_data)
        )
        
        # Add to role-based set
        self.redis_client.sadd(f"agents:role:{role.value}", agent_id)
        
        # Set agent heartbeat
        self._update_heartbeat()
        
        print(f"Agent registered: {agent_id} as {role.value}")
        return True
    
    def _update_heartbeat(self):
        """Update agent heartbeat timestamp"""
        self.redis_client.setex(
            f"agents:heartbeat:{self.agent_id}",
            30,  # 30 second TTL
            datetime.now().isoformat()
        )
    
    def send_message(self, message_type: MessageType, content: Any,
                    recipient_id: Optional[str] = None,
                    recipient_role: Optional[AgentRole] = None,
                    requires_response: bool = False) -> str:
        """
        Send a message to another agent or broadcast to role.
        
        Args:
            message_type: Type of message
            content: Message content
            recipient_id: Specific agent ID (optional)
            recipient_role: Target role for broadcast (optional)
            requires_response: Whether this message requires a response
        
        Returns:
            Message ID
        """
        message_id = str(uuid.uuid4())
        
        message = {
            "message_id": message_id,
            "sender_id": self.agent_id,
            "sender_role": self.agent_role.value,
            "message_type": message_type.value,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "requires_response": requires_response,
            "recipient_id": recipient_id,
            "recipient_role": recipient_role.value if recipient_role else None
        }
        
        # Store message in log
        self.redis_client.lpush(
            "messages:log",
            json.dumps(message)
        )
        
        # Limit log size (keep last 10000 messages)
        self.redis_client.ltrim("messages:log", 0, 9999)
        
        # Publish message
        if recipient_id:
            # Direct message
            channel = f"agent:{recipient_id}"
            self.redis_client.publish(channel, json.dumps(message))
        elif recipient_role:
            # Role-based broadcast
            channel = f"role:{recipient_role.value}"
            self.redis_client.publish(channel, json.dumps(message))
        else:
            # Broadcast to all
            self.redis_client.publish("agents:broadcast", json.dumps(message))
        
        # If requires response, add to pending responses
        if requires_response:
            self.redis_client.setex(
                f"messages:pending:{message_id}",
                300,  # 5 minute timeout
                json.dumps(message)
            )
        
        return message_id
    
    def subscribe_to_messages(self, callback: Callable[[Dict], None]):
        """
        Subscribe to messages for this agent.
        
        Args:
            callback: Function to call when message received
        """
        # Subscribe to direct messages
        self.pubsub.subscribe(f"agent:{self.agent_id}")
        
        # Subscribe to role-based messages
        self.pubsub.subscribe(f"role:{self.agent_role.value}")
        
        # Subscribe to broadcasts
        self.pubsub.subscribe("agents:broadcast")
        
        print(f"Agent {self.agent_id} listening for messages...")
        
        # Listen for messages
        for message in self.pubsub.listen():
            if message["type"] == "message":
                try:
                    msg_data = json.loads(message["data"])
                    callback(msg_data)
                except Exception as e:
                    print(f"Error processing message: {e}")
    
    def request_vote(self, proposal: str, options: List[str],
                    timeout: int = 60) -> Dict[str, Any]:
        """
        Request a democratic vote from all agents.
        
        Args:
            proposal: What is being voted on
            options: List of voting options
            timeout: Vote timeout in seconds
        
        Returns:
            Vote results
        """
        vote_id = str(uuid.uuid4())
        
        vote_data = {
            "vote_id": vote_id,
            "proposal": proposal,
            "options": options,
            "initiated_by": self.agent_id,
            "initiated_at": datetime.now().isoformat(),
            "timeout": timeout
        }
        
        # Store vote
        self.redis_client.setex(
            f"votes:active:{vote_id}",
            timeout,
            json.dumps(vote_data)
        )
        
        # Initialize vote counters
        for option in options:
            self.redis_client.hset(f"votes:results:{vote_id}", option, 0)
        
        # Broadcast vote request
        self.send_message(
            MessageType.VOTE_REQUEST,
            vote_data,
            recipient_role=None  # Broadcast to all
        )
        
        print(f"Vote requested: {vote_id}")
        return vote_data
    
    def cast_vote(self, vote_id: str, option: str) -> bool:
        """
        Cast a vote.
        
        Args:
            vote_id: Vote identifier
            option: Selected option
        
        Returns:
            Success status
        """
        # Check if vote exists
        vote_data = self.redis_client.get(f"votes:active:{vote_id}")
        if not vote_data:
            print(f"Vote {vote_id} not found or expired")
            return False
        
        # Check if already voted
        if self.redis_client.sismember(f"votes:voters:{vote_id}", self.agent_id):
            print(f"Agent {self.agent_id} already voted")
            return False
        
        # Cast vote
        self.redis_client.hincrby(f"votes:results:{vote_id}", option, 1)
        self.redis_client.sadd(f"votes:voters:{vote_id}", self.agent_id)
        
        # Send vote cast message
        self.send_message(
            MessageType.VOTE_CAST,
            {
                "vote_id": vote_id,
                "option": option
            }
        )
        
        print(f"Vote cast: {vote_id} -> {option}")
        return True
    
    def get_vote_results(self, vote_id: str) -> Dict[str, Any]:
        """
        Get current vote results.
        
        Args:
            vote_id: Vote identifier
        
        Returns:
            Vote results with counts
        """
        results = self.redis_client.hgetall(f"votes:results:{vote_id}")
        voters = self.redis_client.smembers(f"votes:voters:{vote_id}")
        
        # Convert counts to integers
        results = {k: int(v) for k, v in results.items()}
        
        # Determine winner
        winner = max(results.items(), key=lambda x: x[1])[0] if results else None
        
        return {
            "vote_id": vote_id,
            "results": results,
            "total_votes": len(voters),
            "voters": list(voters),
            "winner": winner
        }
    
    def request_consensus(self, topic: str, 
                         required_agreement: float = 0.66) -> Dict[str, Any]:
        """
        Request consensus from agents using democratic agreement.
        
        Args:
            topic: What requires consensus
            required_agreement: Minimum agreement threshold (0-1)
        
        Returns:
            Consensus results
        """
        return self.request_vote(
            proposal=f"Consensus required: {topic}",
            options=["agree", "disagree", "abstain"],
            timeout=60
        )
    
    def allocate_task(self, task: Dict[str, Any], 
                     allocation_method: str = "auction") -> Optional[str]:
        """
        Democratically allocate a task to an agent.
        
        Args:
            task: Task to allocate
            allocation_method: Method for allocation (auction, vote, random)
        
        Returns:
            Selected agent ID
        """
        task_id = str(uuid.uuid4())
        
        task_data = {
            "task_id": task_id,
            "task": task,
            "allocation_method": allocation_method,
            "requested_at": datetime.now().isoformat()
        }
        
        # Store task
        self.redis_client.setex(
            f"tasks:pending:{task_id}",
            300,
            json.dumps(task_data)
        )
        
        if allocation_method == "auction":
            # Auction-based allocation
            self.send_message(
                MessageType.TASK_REQUEST,
                task_data,
                recipient_role=AgentRole.PROBLEM_SOLVER
            )
            
            # Wait for bids (simplified for now)
            time.sleep(5)
            
            # Get bids
            bids = self.redis_client.hgetall(f"tasks:bids:{task_id}")
            if bids:
                # Select highest bidder (lowest cost)
                winner = min(bids.items(), key=lambda x: float(x[1]))[0]
                return winner
        
        return None
    
    def log_conversation(self, conversation: Dict[str, Any]):
        """
        Log agent conversation for shared context.
        
        Args:
            conversation: Conversation data to log
        """
        log_entry = {
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "conversation": conversation
        }
        
        # Store in conversation log
        self.redis_client.lpush(
            "conversations:log",
            json.dumps(log_entry)
        )
        
        # Limit log size
        self.redis_client.ltrim("conversations:log", 0, 9999)
        
        # Notify note-takers
        self.send_message(
            MessageType.NOTE_TAKING,
            log_entry,
            recipient_role=AgentRole.NOTE_TAKER
        )
    
    def get_agent_status(self, agent_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get status of an agent or all agents.
        
        Args:
            agent_id: Specific agent ID (optional)
        
        Returns:
            Agent status information
        """
        if agent_id:
            # Get specific agent
            agent_data = self.redis_client.hget("agents:registry", agent_id)
            heartbeat = self.redis_client.get(f"agents:heartbeat:{agent_id}")
            
            if agent_data:
                agent_info = json.loads(agent_data)
                agent_info["last_heartbeat"] = heartbeat
                agent_info["is_alive"] = heartbeat is not None
                return agent_info
        else:
            # Get all agents
            all_agents = self.redis_client.hgetall("agents:registry")
            agents = {}
            
            for aid, data in all_agents.items():
                agent_info = json.loads(data)
                heartbeat = self.redis_client.get(f"agents:heartbeat:{aid}")
                agent_info["last_heartbeat"] = heartbeat
                agent_info["is_alive"] = heartbeat is not None
                agents[aid] = agent_info
            
            return agents
        
        return {}
    
    def get_message_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get message history from the log.
        
        Args:
            limit: Maximum number of messages to retrieve
        
        Returns:
            List of messages
        """
        messages = self.redis_client.lrange("messages:log", 0, limit - 1)
        return [json.loads(msg) for msg in messages]
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform health check on the communication system.
        
        Returns:
            Health status
        """
        try:
            # Test Redis connection
            self.redis_client.ping()
            
            # Get agent counts
            total_agents = self.redis_client.hlen("agents:registry")
            
            # Get message count
            message_count = self.redis_client.llen("messages:log")
            
            return {
                "status": "healthy",
                "redis_connected": True,
                "total_agents": total_agents,
                "message_count": message_count,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python agent_communication.py <action> [args...]")
        print("Actions:")
        print("  register <agent_id> <role> - Register an agent")
        print("  send <message_type> <content> - Send a message")
        print("  vote <proposal> <options> - Request a vote")
        print("  status [agent_id] - Get agent status")
        print("  history [limit] - Get message history")
        print("  health - Check system health")
        sys.exit(1)
    
    action = sys.argv[1]
    hub = AgentCommunicationHub()
    
    if action == "register":
        agent_id = sys.argv[2] if len(sys.argv) > 2 else str(uuid.uuid4())
        role_str = sys.argv[3] if len(sys.argv) > 3 else "problem_solver"
        role = AgentRole[role_str.upper()]
        
        hub.register_agent(agent_id, role)
        print(f"Agent registered: {agent_id}")
    
    elif action == "send":
        msg_type = sys.argv[2] if len(sys.argv) > 2 else "status_update"
        content = sys.argv[3] if len(sys.argv) > 3 else "Hello from agent"
        
        message_type = MessageType[msg_type.upper()]
        msg_id = hub.send_message(message_type, content)
        print(f"Message sent: {msg_id}")
    
    elif action == "vote":
        proposal = sys.argv[2] if len(sys.argv) > 2 else "Test proposal"
        options = sys.argv[3].split(',') if len(sys.argv) > 3 else ["yes", "no"]
        
        vote_data = hub.request_vote(proposal, options)
        print(f"Vote requested: {vote_data['vote_id']}")
    
    elif action == "status":
        agent_id = sys.argv[2] if len(sys.argv) > 2 else None
        status = hub.get_agent_status(agent_id)
        print(json.dumps(status, indent=2))
    
    elif action == "history":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        history = hub.get_message_history(limit)
        print(json.dumps(history, indent=2))
    
    elif action == "health":
        health = hub.health_check()
        print(json.dumps(health, indent=2))
    
    else:
        print(f"Unknown action: {action}")
