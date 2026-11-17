import sys
import os
from flask import Flask, render_template_string, request, jsonify
from decouple import config
from random import choice
from utils import opening_text
from functions.online_ops import (
    find_my_ip, get_latest_news, get_random_advice, get_random_joke,
    get_trending_movies, get_weather_report, play_on_youtube, search_on_google,
    search_on_wikipedia
)
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, open_discord

app = Flask(__name__)

# Generic user representation for anyone using the assistant
USERNAME = config('USER_NAME', default=config('USER', default='User'))
if not USERNAME or USERNAME == os.environ.get('USER'):
    USERNAME = 'User'
BOTNAME = config('BOTNAME', default='Alfred')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ bot_name }} - AI Assistant</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Rajdhani:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #00f0ff;
            --primary-dim: rgba(0, 240, 255, 0.2);
            --bg: #090d16;
            --card-bg: rgba(13, 21, 38, 0.85);
            --text: #e0f8ff;
            --accent: #ff0055;
            --border: rgba(0, 240, 255, 0.3);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Rajdhani', sans-serif;
            background: var(--bg);
            background-image: 
                radial-gradient(circle at 50% 20%, rgba(0, 240, 255, 0.12), transparent 60%),
                linear-gradient(to bottom, #060911, #0a1122);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 900px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        header {
            text-align: center;
            padding: 20px;
            border-bottom: 1px solid var(--border);
            position: relative;
        }
        h1 {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.4rem;
            color: var(--primary);
            text-shadow: 0 0 15px rgba(0, 240, 255, 0.6);
            letter-spacing: 4px;
        }
        .subtitle {
            font-size: 1rem;
            color: rgba(224, 248, 255, 0.6);
            margin-top: 5px;
            letter-spacing: 2px;
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 10px;
            padding: 4px 14px;
            border-radius: 20px;
            background: var(--primary-dim);
            border: 1px solid var(--border);
            font-size: 0.85rem;
            color: var(--primary);
        }
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #00ff66;
            box-shadow: 0 0 8px #00ff66;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
        }

        /* Arc Reactor Animation */
        .reactor-box {
            display: flex;
            justify-content: center;
            margin: 10px 0;
        }
        .arc-reactor {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            border: 2px dashed var(--primary);
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            animation: rotate 12s linear infinite;
            box-shadow: 0 0 25px rgba(0, 240, 255, 0.4);
        }
        .inner-core {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: radial-gradient(circle, #fff, var(--primary));
            box-shadow: 0 0 20px var(--primary);
            animation: glow 3s ease-in-out infinite alternate;
        }
        @keyframes rotate { 100% { transform: rotate(360deg); } }
        @keyframes glow { 0% { opacity: 0.6; } 100% { opacity: 1; } }

        /* Chat Log */
        .chat-box {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            height: 380px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        .message {
            padding: 10px 16px;
            border-radius: 8px;
            max-width: 80%;
            line-height: 1.5;
            font-size: 1.05rem;
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(6px); } to { opacity: 1; transform: translateY(0); } }
        .bot-msg {
            background: rgba(0, 240, 255, 0.1);
            border-left: 3px solid var(--primary);
            align-self: flex-start;
            color: #d8f5ff;
        }
        .user-msg {
            background: rgba(255, 255, 255, 0.08);
            border-right: 3px solid #ffcc00;
            align-self: flex-end;
            color: #fff;
        }
        .sender {
            font-size: 0.75rem;
            color: var(--primary);
            font-weight: 700;
            margin-bottom: 4px;
            letter-spacing: 1px;
        }

        /* Controls */
        .input-bar {
            display: flex;
            gap: 10px;
            background: var(--card-bg);
            padding: 12px;
            border-radius: 12px;
            border: 1px solid var(--border);
        }
        input[type="text"] {
            flex: 1;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px 16px;
            color: #fff;
            font-family: inherit;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.2s;
        }
        input[type="text"]:focus {
            border-color: var(--primary);
            box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
        }
        button {
            background: var(--primary-dim);
            color: var(--primary);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px 20px;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.9rem;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        button:hover {
            background: var(--primary);
            color: #000;
            box-shadow: 0 0 15px var(--primary);
        }
        .mic-btn.active {
            background: var(--accent);
            border-color: var(--accent);
            color: #fff;
            animation: pulse 1s infinite;
        }

        /* Quick Action Chips */
        .quick-actions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
        }
        .chip {
            background: rgba(0, 240, 255, 0.08);
            border: 1px solid rgba(0, 240, 255, 0.2);
            color: rgba(224, 248, 255, 0.8);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        .chip:hover {
            background: var(--primary-dim);
            border-color: var(--primary);
            color: var(--primary);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ bot_name }}</h1>
            <div class="subtitle">VIRTUAL PERSONAL ASSISTANT CORE</div>
            <div class="status-badge">
                <span class="status-dot"></span>
                <span>SYSTEM ONLINE &bull; READY</span>
            </div>
        </header>

        <div class="reactor-box">
            <div class="arc-reactor">
                <div class="inner-core"></div>
            </div>
        </div>

        <div class="chat-box" id="chatBox">
            <div class="message bot-msg">
                <div class="sender">{{ bot_name }}</div>
                Greetings. How may I assist you today? You can type commands below or click the microphone to speak.
            </div>
        </div>

        <div class="input-bar">
            <button id="micBtn" class="mic-btn" title="Toggle Speech Recognition">🎤 Speak</button>
            <input type="text" id="userInput" placeholder="Ask Alfred something (e.g. 'tell me a joke', 'open calculator', 'what is my ip')..." autofocus>
            <button id="sendBtn">Send</button>
        </div>

        <div class="quick-actions">
            <span class="chip" onclick="quickSend('joke')">🎲 Random Joke</span>
            <span class="chip" onclick="quickSend('advice')">💡 Random Advice</span>
            <span class="chip" onclick="quickSend('ip address')">🌐 IP Address</span>
            <span class="chip" onclick="quickSend('open calculator')">🔢 Open Calculator</span>
            <span class="chip" onclick="quickSend('open notepad')">📝 Open Notepad</span>
            <span class="chip" onclick="quickSend('open camera')">📷 Open Camera</span>
            <span class="chip" onclick="quickSend('wikipedia artificial intelligence')">📚 Wikipedia AI</span>
            <span class="chip" onclick="quickSend('trending movies')">🎬 Trending Movies</span>
        </div>
    </div>

    <script>
        const chatBox = document.getElementById('chatBox');
        const userInput = document.getElementById('userInput');
        const sendBtn = document.getElementById('sendBtn');
        const micBtn = document.getElementById('micBtn');

        function appendMessage(sender, text, isBot) {
            const msg = document.createElement('div');
            msg.className = 'message ' + (isBot ? 'bot-msg' : 'user-msg');
            msg.innerHTML = `<div class="sender">${sender}</div>${text.replace(/\\n/g, '<br>')}`;
            chatBox.appendChild(msg);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function speakText(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utter = new SpeechSynthesisUtterance(text);
                utter.rate = 1.0;
                window.speechSynthesis.speak(utter);
            }
        }

        async function sendQuery(query) {
            if (!query.trim()) return;
            appendMessage('You', query, false);
            userInput.value = '';

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                const data = await res.json();
                appendMessage('{{ bot_name }}', data.reply, true);
                speakText(data.reply);
            } catch (err) {
                appendMessage('{{ bot_name }}', 'Error communicating with assistant server: ' + err.message, true);
            }
        }

        function quickSend(cmd) {
            sendQuery(cmd);
        }

        sendBtn.addEventListener('click', () => sendQuery(userInput.value));
        userInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') sendQuery(userInput.value);
        });

        // Web Speech Recognition
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            const recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';

            recognition.onstart = () => {
                micBtn.classList.add('active');
                micBtn.innerText = '🔴 Listening...';
            };
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                userInput.value = transcript;
                sendQuery(transcript);
            };
            recognition.onerror = (e) => {
                console.error("Speech recognition error:", e);
                micBtn.classList.remove('active');
                micBtn.innerText = '🎤 Speak';
            };
            recognition.onend = () => {
                micBtn.classList.remove('active');
                micBtn.innerText = '🎤 Speak';
            };

            micBtn.addEventListener('click', () => {
                try {
                    recognition.start();
                } catch(e) {
                    recognition.stop();
                }
            });
        } else {
            micBtn.style.display = 'none';
        }
    </script>
</body>
</html>
"""

def handle_query(query):
    q = query.lower().strip()
    
    if 'who are you' in q or 'your name' in q or 'what are you' in q:
        return f"I am {BOTNAME}, your personal virtual assistant, at your service."
    elif 'open notepad' in q:
        open_notepad()
        return "Opening Notepad / TextEdit for you."
    elif 'open discord' in q:
        open_discord()
        return "Launching Discord."
    elif 'open command prompt' in q or 'open cmd' in q:
        open_cmd()
        return "Opening Terminal."
    elif 'open camera' in q:
        open_camera()
        return "Opening Camera."
    elif 'open calculator' in q:
        open_calculator()
        return "Opening Calculator."
    elif 'ip address' in q:
        try:
            ip = find_my_ip()
            return f"Your current IP address is {ip}."
        except Exception as e:
            return f"Could not determine IP address: {e}"
    elif 'joke' in q:
        try:
            return get_random_joke()
        except Exception as e:
            return f"Couldn't fetch a joke right now ({e})."
    elif 'advice' in q:
        try:
            return get_random_advice()
        except Exception as e:
            return f"Couldn't fetch advice right now ({e})."
    elif 'trending movies' in q:
        try:
            movies = get_trending_movies()
            return "Trending Movies:\\n• " + "\\n• ".join(movies)
        except Exception as e:
            return f"Could not fetch movies: {e}"
    elif 'news' in q:
        try:
            news = get_latest_news()
            return "Latest News:\\n• " + "\\n• ".join(news)
        except Exception as e:
            return f"Could not fetch news: {e}"
    elif 'wikipedia' in q:
        topic = q.replace('wikipedia', '').replace('search on', '').strip()
        if not topic:
            return "What would you like me to look up on Wikipedia?"
        try:
            return search_on_wikipedia(topic)
        except Exception as e:
            return f"Wikipedia lookup failed: {e}"
    elif 'youtube' in q:
        video = q.replace('youtube', '').replace('play', '').replace('on', '').strip()
        play_on_youtube(video if video else 'trending')
        return f"Playing '{video}' on YouTube."
    elif 'search on google' in q or 'search google' in q:
        term = q.replace('search on google', '').replace('search google', '').strip()
        search_on_google(term)
        return f"Searching Google for '{term}'."
    elif 'exit' in q or 'bye' in q:
        return "Goodbye sir! Have a great day!"
    else:
        # Default fallback: try wikipedia summary
        try:
            res = search_on_wikipedia(q)
            return res
        except Exception:
            return f"I heard '{query}'. I don't have a direct skill for that yet, but you can ask for jokes, advice, IP address, system apps, or search Wikipedia."

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, bot_name=BOTNAME, user_name=USERNAME)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    query = data.get('query', '')
    reply = handle_query(query)
    return jsonify({ 'reply': reply, 'query': query })

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({ 'bot': BOTNAME, 'user': USERNAME, 'status': 'online', 'port': 5002 })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    print(f"Starting {BOTNAME} web server on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
