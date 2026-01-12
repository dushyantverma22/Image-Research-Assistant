# 🧠 Image Research Assistant

An end-to-end **Agentic AI system** that analyzes images, extracts context, and performs fact-based research—demonstrating production-grade LLMOps, cloud deployment, and DevOps practices.

**Live Demo:** `http://54.147.190.138:7860` 

---

## 🎯 Overview

This project combines **vision intelligence**, **web research**, and **agentic reasoning** into a containerized, cloud-deployed application. It's designed to showcase:

- ✅ **Agentic AI Architecture** – LangGraph-based multi-step reasoning
- ✅ **Tool Orchestration** – MCP (Model Context Protocol) for extensible tool routing
- ✅ **Production LLMOps** – Proper error handling, state management, and logging
- ✅ **Cloud DevOps** – AWS EC2, ECR, GitHub Actions CI/CD pipeline
- ✅ **Containerization** – Docker with optimized layers and security best practices
- ✅ **Interactive UI** – Gradio web interface for seamless user experience

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User (Browser)                       │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
         ┌─────────────────────────┐
         │    Gradio UI (EC2)      │
         │   Port 7860             │
         └────────────┬────────────┘
                      │
                      ▼
         ┌─────────────────────────────────────────────┐
         │    LangGraph Agent Orchestrator             │
         │  (State Management + Reasoning Workflow)    │
         └─────────────────┬──────────────────────────┘
                          │
          ┌───────────────┴───────────────┐
          │                               │
          ▼                               ▼
   ┌──────────────────┐        ┌──────────────────────┐
   │ Vision MCP       │        │ Wikipedia MCP        │
   │ Server           │        │ Server               │
   │                  │        │                      │
   │ → OpenAI Vision  │        │ → Wikipedia API      │
   │   API (GPT-4o)   │        │   (Fact-checking)    │
   └──────────────────┘        └──────────────────────┘
```

### Workflow

1. **User Input** – Upload image + enter query in Gradio UI
2. **Agent Initialization** – LangGraph agent receives inputs
3. **Visual Analysis** – Vision MCP tool extracts subject/context from image
4. **Research Phase** – Wikipedia MCP tool fetches factual information
5. **Composition** – Agent synthesizes final response using tool outputs
6. **Display** – Results rendered in Gradio UI

---

## 🚀 Key Features

| Feature | Details |
|---------|---------|
| 🖼️ **Image Understanding** | OpenAI Vision API extracts main subjects, landmarks, concepts |
| 📚 **Automated Research** | Wikipedia integration for fact-based summaries |
| 🧠 **Agentic Reasoning** | LangGraph enforces multi-step reasoning without hallucination |
| 🔧 **Tool Routing** | MCP-based architecture for extensible tool integration |
| 🌐 **Web Interface** | Gradio UI for intuitive image upload and querying |
| 🐳 **Containerization** | Docker for reproducibility across environments |
| ☁️ **Cloud Native** | AWS EC2 + ECR + GitHub Actions for automated deployment |
| 🔐 **Secure Secrets** | GitHub Secrets + environment variables for API keys |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Gradio |
| **Orchestration** | LangGraph |
| **Tool Protocol** | MCP (Model Context Protocol) |
| **LLM** | OpenAI GPT-4o-mini |
| **Vision** | OpenAI Vision API |
| **Research** | Wikipedia API |
| **Containerization** | Docker |
| **CI/CD** | GitHub Actions |
| **Cloud** | AWS EC2, ECR |
| **Runtime** | Python 3.10+ |

---

## 📂 Project Structure

```
Image-Research-Assistant/
├── mcp_client.py                 # Main orchestrator + Gradio UI
├── visual_analysis_server.py     # Vision MCP server (subprocess)
├── research_server.py            # Wikipedia MCP server (subprocess)
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container definition
├── .dockerignore                 # Docker build optimization
├── .github/
│   └── workflows/
│       └── aws.yaml              # CI/CD pipeline (ECR + EC2)
├── image/                        # Sample images for testing
├── setup.py                      # Package configuration
├── README.md                     # Project documentation
└── .gitignore                    # Git ignore rules
```

---

## 🚀 Quick Start

### Local Development

#### Prerequisites
- Python 3.10+
- Docker & Docker Compose
- AWS Account (for deployment)
- GitHub Account (for CI/CD)
- OpenAI API Key
- GitHub Personal Access Token (for CI/CD)

#### Installation

```bash
# Clone repository
git clone https://github.com/dushyantverma22/Image-Research-Assistant.git
cd Image-Research-Assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your_openai_api_key

# Run locally
python mcp_client.py
```

Access Gradio UI at: `http://localhost:7860`

---

## 🐳 Docker Setup

### Build Docker Image

```bash
docker build -t image-assistant:latest .
```

### Run Container Locally

```bash
docker run -d \
  -p 7860:7860 \
  -e OPENAI_API_KEY=your_openai_api_key \
  --name image-assistant \
  image-assistant:latest
```

### View Logs

```bash
docker logs -f image-assistant
```

### Stop Container

```bash
docker stop image-assistant
docker rm image-assistant
```

---

## ☁️ AWS Deployment (End-to-End)

### Step 1: Create EC2 Instance

```bash
# Launch EC2 (Ubuntu 22.04, t3.medium minimum)
# Security Group: Allow inbound HTTP (80) and custom (7860)
# Key pair: Create and store safely
```

### Step 2: Configure Self-Hosted Runner on EC2

```bash
# SSH into EC2
ssh -i your-key.pem ubuntu@<ec2-public-ip>

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
sudo apt install docker.io -y
sudo usermod -aG docker $USER

# Install GitHub Actions Runner
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-*.tar.gz \
  -L https://github.com/actions/runner/releases/download/v2.313.0/actions-runner-linux-x64-2.313.0.tar.gz
tar xzf actions-runner-linux-x64-*.tar.gz

# Configure runner (interactive)
./config.sh --url https://github.com/yourusername/Image-Research-Assistant \
            --token <RUNNER_TOKEN>

# Install runner as service
sudo ./svc.sh install
sudo ./svc.sh start
```

### Step 3: Configure GitHub Secrets

In your GitHub repo, go to **Settings → Secrets and variables → Actions** and add:

```
AWS_ACCESS_KEY_ID          = your_aws_access_key
AWS_SECRET_ACCESS_KEY      = your_aws_secret_key
AWS_DEFAULT_REGION         = us-east-1
ECR_REPO                   = your_account_id.dkr.ecr.us-east-1.amazonaws.com/image-assistant
OPENAI_API_KEY             = your_openai_api_key
EC2_HOST                   = your-ec2-public-ip
EC2_USER                   = ubuntu
EC2_KEY                    = (contents of your SSH key)
```

### Step 4: Push to GitHub

```bash
git add .
git commit -m "Initial commit: Image Research Assistant"
git push origin main
```

**CI/CD Pipeline Automatically:**
- ✅ Builds Docker image
- ✅ Pushes to Amazon ECR
- ✅ Deploys to EC2
- ✅ Restarts Gradio service

### Step 5: Access Application

```
http://<your-ec2-public-ip>:7860
```

---

## 🔐 Secrets Management

All sensitive information is managed via **GitHub Secrets** and injected at runtime:

```yaml
# In .github/workflows/aws.yaml
env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

**Never commit secrets to repository.** Use `.gitignore` for `.env` files.

---

## 🧠 Agentic Workflow Details

### LangGraph Agent State

```python
class AgentState(TypedDict):
    image_path: str
    user_query: str
    vision_result: str
    research_result: str
    final_answer: str
    error: Optional[str]
```

### Node Functions

1. **validate_input()** – Check image exists and query is valid
2. **analyze_vision()** – Call Vision MCP tool to extract subject
3. **research_topic()** – Call Wikipedia MCP tool for facts
4. **compose_response()** – Synthesize final answer using LLM
5. **handle_error()** – Graceful error recovery

### Tool Invocation Pattern

```
Agent → MCP Router → Vision/Wikipedia Servers → APIs → Results → Agent
```

No hallucination—agent strictly bound to tool outputs.

---

## 📊 Sample Use Cases

### Use Case 1: Historical Landmarks

**Input:**
- Image: Pyramids of Giza
- Query: "Describe this monument and its historical significance"

**Output:**
```
Subject Identified: Great Pyramids of Giza
Historical Facts:
- Built during Old Kingdom Egypt (2580-2510 BCE)
- Tombs of Pharaohs Khufu, Khafre, and Menkaure
- Original height: 146.5 meters (Khufu's pyramid)
- Constructed by estimated 100,000+ workers over 20 years
- Only surviving Wonder of the Ancient World
```

### Use Case 2: Natural Phenomena

**Input:**
- Image: Aurora Borealis
- Query: "Explain the science behind this phenomenon"

**Output:**
```
Subject Identified: Aurora Borealis (Northern Lights)
Scientific Explanation:
- Caused by solar wind interaction with Earth's magnetosphere
- Occurs at high latitudes (>60° North/South)
- Visible light from excited oxygen and nitrogen atoms
- Peak activity during solar maximum (11-year cycle)
- Typically green, red, purple, or blue colors
```

---

## 🛠️ Engineering Challenges Solved

| Challenge | Solution |
|-----------|----------|
| **Docker build failures** | Optimized layer caching, multi-stage builds |
| **Environment variables in containers** | Use `docker run -e` and GitHub Secrets |
| **Gradio path handling** | Absolute paths, proper working directory setup |
| **MCP subprocess orchestration** | Context managers for clean startup/shutdown |
| **Self-hosted runner connectivity** | Firewall rules, security groups, NAT handling |
| **AWS networking** | Security group ingress rules, Elastic IPs |
| **API rate limiting** | Exponential backoff, caching mechanisms |
| **Container startup time** | Health checks, dependency management |

---

## 🚨 Troubleshooting

### Docker Build Issues

```bash
# Clear Docker cache
docker system prune -a

# Rebuild with no cache
docker build --no-cache -t image-assistant:latest .
```

### MCP Server Not Responding

```bash
# Check logs
docker logs image-assistant

# Verify port binding
docker ps -a
netstat -tuln | grep 7860
```

### EC2 Connection Issues

```bash
# Test SSH
ssh -i key.pem ubuntu@<ip> "echo connected"

# Check security group
aws ec2 describe-security-groups --group-ids sg-xxxxx
```

### OpenAI API Errors

```bash
# Verify API key
echo $OPENAI_API_KEY

# Test connectivity
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

---

## 📈 Performance Optimization

### Docker Optimization
- Multi-stage builds to reduce image size
- Layer caching strategy for faster rebuilds
- Minimal base images (python:3.10-slim)

### LLM Optimization
- GPT-4o-mini for cost-effective inference
- Prompt caching for repeated queries
- Token counting for cost estimation

### Infrastructure Optimization
- t3.medium EC2 for cost/performance balance
- Auto-restart policies for fault tolerance
- Health checks in Gradio

---

## 🔄 CI/CD Pipeline Flow

```
┌─ GitHub Push (main branch)
│
├─ GitHub Actions Triggered
│
├─ Build Docker Image
│  └─ ECR Login
│  └─ Build & Tag Image
│  └─ Push to ECR
│
├─ Deploy to EC2
│  └─ SSH into instance
│  └─ Pull latest image from ECR
│  └─ Stop old container
│  └─ Run new container
│  └─ Verify health check
│
└─ ✅ Live (zero downtime deployment)
```

---

## 📚 Learning Resources

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph/)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [OpenAI Vision API Guide](https://platform.openai.com/docs/guides/vision)
- [Docker Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [AWS EC2 User Guide](https://docs.aws.amazon.com/ec2/)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the **MIT License**. See `LICENSE` file for details.

---

## 👨‍💻 Author

**Dushyant Verma**  
Data Scientist | LLM Engineer | ML Engineer

📧 Email: [dushyantdchss@gmail.com](mailto:dushyantdchss@gmail.com)  
🔗 LinkedIn: [linkedin.com/in/dushyant-verma](https://linkedin.com/in/dushyant-verma)  
🐙 GitHub: [@dushyantverma](https://github.com/dushyantverma)

---

## 🙌 Acknowledgments

- OpenAI for GPT-4o Vision API
- Anthropic for MCP specification
- Wikipedia API for factual data
- AWS & GitHub for cloud infrastructure
- LangChain community for LLM frameworks

---

## 📞 Support

Have questions or issues? Please:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Open a GitHub Issue with detailed description
3. Include logs: `docker logs image-assistant`
4. Provide your environment details (OS, Python version, Docker version)

---

**⭐ If this project helped you, please star the repository!**

*Last updated: January 2026*