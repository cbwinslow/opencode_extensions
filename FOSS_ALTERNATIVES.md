# FOSS Alternatives Guide

## 🌟 Why FOSS-Only?

This opencode extensions project is committed to **100% Free and Open Source Software**. This ensures:
- **Data sovereignty** - Your data stays on your infrastructure
- **No vendor lock-in** - Complete control over your tools
- **Privacy by design** - No tracking or data harvesting
- **Community support** - Transparent development and community-driven improvements
- **Cost freedom** - No licensing fees or subscription costs

## 🔄 Proprietary → FOSS Migration

### Communication Platforms

| Proprietary | FOSS Alternative | Self-Hostable | Key Features |
|-------------|------------------|---------------|--------------|
| Slack | **Mattermost** | ✅ | Channels, integrations, mobile apps |
| Discord | **Matrix** | ✅ | Federation, E2E encryption, bridges |
| Microsoft Teams | **Element** (Matrix) | ✅ | Video calls, screen sharing, file sharing |
| Zoom | **Jitsi Meet** | ✅ | WebRTC, no downloads, recording |

### Project Management

| Proprietary | FOSS Alternative | Self-Hostable | Key Features |
|-------------|------------------|---------------|--------------|
| Jira | **Redmine** | ✅ | Issue tracking, Gantt charts, plugins |
| Trello | **Kanboard** | ✅ | Kanban boards, swimlanes, automation |
| Asana | **Taiga** | ✅ | Agile, Scrum, Kanban, issues |
| GitHub Projects | **Gitea** | ✅ | Git hosting, issues, projects, CI/CD |

### Note-taking & Documentation

| Proprietary | FOSS Alternative | Self-Hostable | Key Features |
|-------------|------------------|---------------|--------------|
| Notion | **Nextcloud Notes** | ✅ | Markdown, collaboration, mobile |
| Confluence | **BookStack** | ✅ | WYSIWYG, permissions, search |
| Evernote | **Joplin** | ✅ | End-to-end encryption, sync |
| Google Docs | **Collabora Online** | ✅ | Real-time collaboration, LibreOffice |

### AI & Machine Learning

| Proprietary | FOSS Alternative | Self-Hostable | Key Features |
|-------------|------------------|---------------|--------------|
| OpenAI GPT | **Ollama + Llama2** | ✅ | Local processing, privacy |
| Claude | **Mistral** | ✅ | Open weights, commercial use |
| GitHub Copilot | **CodeLlama** | ✅ | Code completion, local |
| DALL-E | **Stable Diffusion** | ✅ | Image generation, fine-tuning |

### Development Tools

| Proprietary | FOSS Alternative | Self-Hostable | Key Features |
|-------------|------------------|---------------|--------------|
| GitHub | **Gitea** | ✅ | Lightweight, easy setup |
| GitLab | **Gitea/Gogs** | ✅ | Git hosting, CI/CD |
| Travis CI | **Woodpecker CI** | ✅ | Simple, fast, Docker-native |
| CircleCI | **Drone CI** | ✅ | Container-based, scalable |

## 🚀 Quick Setup Guide

### 1. Communication Setup

#### Mattermost (Slack Alternative)
```bash
# Docker setup
docker run -d --name mattermost \
  -p 8065:8065 \
  mattermost/mattermost-team-edition
```

#### Matrix (Discord Alternative)
```bash
# Docker setup
docker run -d --name synapse \
  -p 8008:8008 \
  -v $(pwd)/data:/data \
  matrixdotorg/synapse:latest
```

### 2. Project Management Setup

#### Redmine (Jira Alternative)
```bash
# Docker setup
docker run -d --name redmine \
  -p 3000:3000 \
  -v redmine-data:/usr/src/redmine/files \
  redmine:latest
```

#### Gitea (GitHub Alternative)
```bash
# Docker setup
docker run -d --name gitea \
  -p 3000:3000 \
  -p 222:22 \
  -v gitea-data:/data \
  gitea/gitea:latest
```

### 3. AI/ML Setup

#### Ollama (OpenAI Alternative)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama2
ollama pull codellama
ollama pull mistral
```

### 4. Note-taking Setup

#### Nextcloud Notes (Notion Alternative)
```bash
# Docker setup with Nextcloud
docker run -d --name nextcloud \
  -p 8080:80 \
  -v nextcloud-data:/var/www/html \
  nextcloud:latest
```

## 🔧 Configuration Examples

### MCP Server Configuration

All MCP servers now use FOSS alternatives:

```json
{
  "name": "Mattermost MCP Server",
  "self_hosted": true,
  "open_source": "https://github.com/mattermost/mattermost-server",
  "auth_type": "token",
  "token_source": "file"
}
```

### Token Management

Use the built-in FOSS token manager:

```bash
# Store a token
python3 cli.py foss_token store mattermost "your-token-here"

# List all tokens
python3 cli.py foss_token list

# Generate a secure token
python3 cli.py foss_token generate my-service 32
```

## 📋 Migration Checklist

### Before Migration
- [ ] Export data from proprietary services
- [ ] Identify critical integrations
- [ ] Plan user training
- [ ] Set up self-hosting infrastructure

### During Migration
- [ ] Deploy FOSS alternatives
- [ ] Configure authentication
- [ ] Migrate data
- [ ] Set up integrations
- [ ] Test functionality

### After Migration
- [ ] Decommission proprietary services
- [ ] Update documentation
- [ ] Train users
- [ ] Monitor performance

## 🛡️ Security Considerations

### Self-Hosting Security
- Use HTTPS/TLS for all services
- Implement proper authentication
- Regular security updates
- Backup strategies
- Network segmentation

### Token Security
- Local encryption with Fernet
- Regular token rotation
- Access logging
- Secure storage permissions
- Audit trails

## 🤝 Community Resources

### Support Communities
- **Mattermost**: https://community.mattermost.com
- **Matrix**: https://matrix.org/community
- **Redmine**: https://www.redmine.org/projects/redmine/boards
- **Gitea**: https://discourse.gitea.io
- **Ollama**: https://github.com/ollama/ollama/discussions

### Documentation
- **Mattermost Docs**: https://docs.mattermost.com
- **Matrix Spec**: https://spec.matrix.org
- **Redmine Guide**: https://www.redmine.org/guide
- **Gitea Docs**: https://docs.gitea.io
- **Ollama Docs**: https://github.com/ollama/ollama/blob/main/docs.md

## 🎯 Benefits Realized

### Cost Savings
- **Zero licensing fees** - All software is free
- **Infrastructure control** - Use your existing servers
- **No vendor lock-in** - Switch providers anytime

### Data Privacy
- **Local processing** - Data never leaves your infrastructure
- **No tracking** - FOSS projects don't track users
- **Full control** - You decide what data to collect

### Customization
- **Source code access** - Modify as needed
- **Plugin ecosystems** - Extend functionality
- **API access** - Integrate with anything

---

**Remember**: Every proprietary service has a FOSS alternative. Choose freedom, choose privacy, choose control!