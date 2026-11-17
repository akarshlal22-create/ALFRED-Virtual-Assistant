# Alfred — Virtual Personal Assistant 🎙️🤖

An intelligent, cross-platform personal AI assistant built with Python. Alfred features dual interfaces: an interactive **Voice/CLI Terminal** and a sleek, futuristic **Cyberpunk Web Dashboard** running on `localhost:5002`.

---

## ✨ Features

- **Dual Interaction Modes**:
  - **Terminal / Voice Mode**: Voice recognition with SpeechRecognition & PyAudio, with automatic console fallback for typing.
  - **Cyberpunk Web Dashboard**: Interactive web app with real-time browser speech synthesis, voice input (Web Speech API), and visual arc-reactor telemetry.
- **Cross-Platform Support**: Seamlessly works on **macOS**, **Windows**, and **Linux**.
- **System Automation**:
  - Open Calculator, Text Editor / Notepad, Camera, Terminal / Command Prompt, and Discord.
- **Online Utilities**:
  - 🌐 Check Public IP address
  - 📚 Wikipedia instant summary search
  - 🎥 Play videos directly on YouTube
  - 🔍 Quick Google search
  - 💬 Send WhatsApp messages
  - 📧 Send automated emails via SMTP
  - 🎲 Random jokes and life advice
  - 🎬 Daily trending movies (via TMDB API)
  - 📰 Top news headlines (via NewsAPI)
  - 🌤️ Live city weather reports (via OpenWeatherMap API)

---

## 📁 Project Structure

```text
├── app.py                # Flask Web Dashboard & REST API (localhost:5002)
├── main.py               # Terminal Voice & Text Assistant
├── run.sh                # Quick launch script (macOS/Linux)
├── utils.py              # Assistant speech phrases & helpers
├── requirements.txt      # Project dependencies
├── .env.example          # Sample environment configuration template
├── functions/
│   ├── online_ops.py     # Web APIs (Wikipedia, YouTube, Weather, News, etc.)
│   └── os_ops.py         # Cross-platform application launchers
└── README.md
```

---

## 🚀 Getting Started

### 1. Prerequisites

- **Python 3.8+**
- **PortAudio** (required for microphone input via PyAudio):
  - **macOS**: `brew install portaudio`
  - **Ubuntu/Debian**: `sudo apt install portaudio19-dev python3-pyaudio`
  - **Windows**: PyAudio installs directly via pip.

---

### 2. Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/akarshlal22-create/Alfred---Virtual-Assistant.git
   cd Alfred---Virtual-Assistant
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # On macOS/Linux
   # or
   .\venv\Scripts\activate       # On Windows
   ```

3. **Install dependencies**:
   - **For Web Dashboard & Cloud Deployment (Render/Railway)**:
     ```bash
     pip install -r requirements.txt
     ```
   - **For Local Terminal Voice Recognition (optional)**:
     ```bash
     # First install portaudio:
     # macOS: brew install portaudio
     # Ubuntu/Debian: sudo apt install portaudio19-dev
     pip install -r requirements-local.txt
     ```

4. **Configure Environment Variables**:
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   *(Optional)* Edit `.env` to add your API keys for Weather, News, or Movies:
   ```env
   USER_NAME=User
   BOTNAME=Alfred
   NEWS_API_KEY=your_key_here
   OPENWEATHER_APP_ID=your_key_here
   TMDB_API_KEY=your_key_here
   ```

---

## 🖥️ Usage

### Option A: Web Dashboard (Recommended)

Start the local web server:
```bash
python app.py
```
Open **[http://localhost:5002](http://localhost:5002)** in your browser.
- Click **🎤 Speak** for browser-based voice commands.
- Type commands in the prompt or click quick-action chips.
- Alfred speaks responses back aloud using speech synthesis.

---

### Option B: Docker Deployment (Containerized)

Build and run using **Docker**:
```bash
# Build the Docker image
docker build -t alfred-assistant .

# Run the container
docker run -d -p 5002:5002 --name alfred alfred-assistant
```

Or using **Docker Compose**:
```bash
docker compose up -d
```
Once started, visit **[http://localhost:5002](http://localhost:5002)** in your browser.

To stop the container:
```bash
docker compose down
# or
docker stop alfred && docker rm alfred
```

---

### Option C: Terminal (Voice or Text Mode)

Using the launcher script:
```bash
# Voice mode (default):
./run.sh

# Text console mode:
./run.sh --text
```

Or directly with Python:
```bash
python main.py          # Interactive mode (Voice or Text)
python main.py --text   # Text-only console mode
```

---

## 🗣️ Supported Voice / Text Commands

| Command | Action |
| :--- | :--- |
| `who are you` / `your name` | Introduces Alfred |
| `joke` | Tells a random programming/dad joke |
| `advice` | Provides random life advice |
| `ip address` | Checks and displays current public IP |
| `wikipedia <topic>` | Summarizes a topic from Wikipedia |
| `youtube <search>` | Searches and plays video on YouTube |
| `search on google <term>` | Performs a Google search |
| `open calculator` | Opens native Calculator app |
| `open notepad` | Opens TextEdit / Notepad |
| `open camera` | Opens Photo Booth / Camera |
| `open command prompt` | Launches Terminal / CMD |
| `open discord` | Launches Discord |
| `weather` | Live weather report *(requires API key)* |
| `news` | Top 5 headlines *(requires API key)* |
| `trending movies` | Top trending movies *(requires API key)* |
| `send an email` | Prompts for recipient, subject, and message |
| `exit` / `stop` | Gracefully closes the assistant |

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
