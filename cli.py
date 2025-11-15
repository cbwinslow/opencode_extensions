#!/usr/bin/env python3

import sys
import subprocess

def run_command(cmd):
    subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cli.py <command> [args...]")
        print("Commands: review, test, deploy, validate_openapi, fetch_data, convert_format, handle_webhook, automate, manage_linear, get_token, foss_token, memory, analyze_code, create_project, memory_config, hierarchical_memory, vector_db, agent_comm, multiagent")
        sys.exit(1)
    command = sys.argv[1]
    args = sys.argv[2:]
    if command == "review":
        run_command(f"python agents/code_reviewer.py {' '.join(args)}")
    elif command == "test":
        run_command("python agents/tester.py")
    elif command == "deploy":
        run_command(f"python agents/deployer.py {' '.join(args)}")
    elif command == "validate_openapi":
        run_command(f"python tools/openapi_validator.py {' '.join(args)}")
    elif command == "fetch_data":
        run_command(f"python tools/data_fetcher.py {' '.join(args)}")
    elif command == "convert_format":
        run_command(f"python tools/format_converter.py {' '.join(args)}")
    elif command == "handle_webhook":
        run_command(f"python integrations/webhook_handler.py {' '.join(args)}")
    elif command == "automate":
        run_command(f"python integrations/automation.py {' '.join(args)}")
    elif command == "manage_linear":
        run_command(f"python integrations/linear_manager.py {' '.join(args)}")
    elif command == "get_token":
        run_command(f"python configs/token_manager.py {' '.join(args)}")
    elif command == "memory":
        run_command(f"python tools/memory_manager.py {' '.join(args)}")
    elif command == "analyze_code":
        run_command(f"python tools/code_analyzer.py {' '.join(args)}")
    elif command == "create_project":
        run_command(f"python tools/project_manager.py {' '.join(args)}")
    elif command == "memory_config":
        run_command(f"python configs/memory_config.py {' '.join(args)}")
    elif command == "hierarchical_memory":
        run_command(f"python tools/hierarchical_memory.py {' '.join(args)}")
    elif command == "foss_token":
        run_command(f"python configs/foss_token_manager.py {' '.join(args)}")
    elif command == "vector_db":
        run_command(f"python tools/vector_database.py {' '.join(args)}")
    elif command == "agent_comm":
        run_command(f"python tools/agent_communication.py {' '.join(args)}")
    elif command == "multiagent":
        run_command(f"python agents/multiagent_coordinator.py {' '.join(args)}")
    else:
        print(f"Unknown command: {command}")