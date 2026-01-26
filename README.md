# HIGH ERA | Automated Creative Infrastructure

**Established 2026.**

High Era is the operating system for modern marketing agencies. It replaces the chaos of scattered briefs, lost context, and manual asset generation with a unified, intelligent "Agency Memory."

![High Era Terminal](https://storage.googleapis.com/marketing-copy-assets/images/generated_c46bed9c-bf11-44f3-8aba-6dcf6d121b8e.png)

## Two Ways to Run High Era

We believe in the power of open source and the convenience of managed services. Choose the path that fits your ambition.

### 1. The Managed Studio (Recommended)
**For Marketing Directors, Agencies, and Teams.**

Skip the infrastructure setup. Get instant access to the full High Era suite, including our premium Twin-Engine video generation, priority processing, and white-glove support.

- ✅ **Instant Access:** Start briefing in 30 seconds.
- ✅ **Managed Infrastructure:** We handle the GPUs, queues, and uptime.
- ✅ **Enterprise Security:** SOC2 compliant (roadmap), encrypted Dossiers.
- ✅ **Zero Maintenance:** Continuous updates and new skills automatically added.

[**→ Start Your Studio ($297/mo)**](https://high-era.com) | [View Pricing](https://high-era.com/pricing)

### 2. The Open Source Core
**For Engineers, Hackers, and Builders.**

Run the core engine on your own infrastructure. You have full control over the code, the models, and the data. You are the architect.

- 🛠 **Full Control:** Modify the skills, tweak the prompts, own the stack.
- 🛠 **Self-Hosted:** Run on your own GCP project or local machine.
- 🛠 **Community Driven:** Contribute to the skill library.

[**→ View Deployment Guide**](#deployment)

---

## Key Capabilities

### 📂 The Dossier (Contextual Memory)
Stop re-explaining your brand. High Era remembers your products, audiences, and value propositions. 
- **Persists Context:** Briefs are saved and indexed.
- **Auto-Priming:** The AI knows your voice before you write a word.

### ⚡️ Twin-Engine Workflow (Async Generation)
Don't wait for the progress bar.
- **Engine 1 (Synchronous):** Instant strategy, copy, and ideas.
- **Engine 2 (Asynchronous):** Background workers handle heavy lifting (Video rendering, Deep Research).
- **Notification System:** Queue 10 campaigns, get notified when they're done.

### 🧠 The Skill Library (Madison Avenue Logic)
We don't just "prompt." We execute proven frameworks.
- **25+ Specialized Skills:** From "Hemingway-style Copy" to "Kling Video Scripts".
- **Rigorous Checklists:** Every output is self-evaluated before you see it.

---

## Local Development (Self-Hosted)

### Prerequisites
- Python 3.10+
- Node.js 18+
- Google Cloud Project (Firestore, Pub/Sub, Storage)
- Anthropic API Key
- FAL.ai Key (for video/image generation)

### Quick Start

1.  **Clone the Repo**
    ```bash
    git clone https://github.com/high-era/core.git
    cd high-era
    ```

2.  **Configure Environment**
    ```bash
    cp .env.example .env
    # Add your API keys to .env
    ```

3.  **Start Backend (FastAPI)**
    ```bash
    pip install -r requirements.txt
    python3 -m uvicorn service.main:app --reload --port 8080
    ```

4.  **Start Frontend (SvelteKit)**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

5.  **Open the Terminal**
    Visit `http://localhost:3000` to access your local High Era instance.

## Deployment

The system is designed for **Google Cloud Run**.

```bash
# Deploy Backend
gcloud run deploy high-era-api --source .

# Deploy Frontend
cd frontend
gcloud run deploy high-era-ui --source .
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed architecture documentation.

---

## License

High Era is open-source software licensed under the [MIT license](LICENSE).
You are free to use, modify, and distribute this software for private or commercial use.