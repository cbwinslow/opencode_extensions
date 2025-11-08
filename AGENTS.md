# AGENTS.md

## Build/Lint/Test Commands

- **Run all tests**: `python3 cli.py test` or `python3 agents/tester.py`
- **Run single test**: `python3 -m pytest path/to/test_file.py` (for Python) or `npm test -- path/to/test_file.js` (for JavaScript)
- **Code review**: `python3 cli.py review <file_path>` or `python3 agents/code_reviewer.py <file_path>`
- **Validate OpenAPI**: `python3 cli.py validate_openapi <spec_file>`
- **Memory management**: `python3 cli.py memory <action>` or `python3 cli.py hierarchical_memory <action>`
- **Token management**: `python3 cli.py foss_token <action>`
- **Code analysis**: `python3 cli.py analyze_code <action>`
- **Project creation**: `python3 cli.py create_project <action>`

## FOSS-First Policy

This project exclusively uses Free and Open Source Software (FOSS). All integrations, tools, and dependencies are open source.

### Supported FOSS Services
- **Communication**: Mattermost, Matrix (self-hosted)
- **Project Management**: Redmine, Gitea (self-hosted)
- **Note-taking**: Nextcloud Notes (self-hosted)
- **AI/ML**: Ollama (local models), Llama2, Mistral, CodeLlama
- **Authentication**: Local encrypted token storage

### Forbidden Proprietary Services
- No Slack, Discord, or proprietary communication platforms
- No GitHub, GitLab (proprietary hosting), use Gitea instead
- No OpenAI, Anthropic, or proprietary AI services
- No Notion, Jira, or proprietary SaaS platforms

## Code Style Guidelines

### Python
- Use shebang `#!/usr/bin/env python3` at top of executable scripts
- Import standard library first, then third-party imports
- Use snake_case for variables and functions, PascalCase for classes
- Line length limit: 100 characters (enforced by code reviewer)
- Handle exceptions with try/except blocks, include meaningful error messages
- Use subprocess.run() for external commands with capture_output=True, text=True
- Prefer FOSS libraries over proprietary alternatives

### General
- Use descriptive function and variable names
- Add TODO/FIXME comments sparingly, address them promptly
- Follow existing patterns in the codebase for consistency
- Use JSON for configuration and data interchange
- Include proper error handling for network requests and file operations
- All external integrations must be self-hostable FOSS solutions
- Token storage must use local encryption, never proprietary vaults

## Security Guidelines
- All tokens stored locally with Fernet encryption
- No external authentication services
- Self-hosted infrastructure preferred
- Regular token rotation supported
- Export/import functionality for backup/migration