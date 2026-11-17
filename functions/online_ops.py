import requests
import wikipedia
import webbrowser
try:
    import pywhatkit as kit
except Exception:
    kit = None
from email.message import EmailMessage
import smtplib
from decouple import config

NEWS_API_KEY = config("NEWS_API_KEY", default="")
OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID", default="")
TMDB_API_KEY = config("TMDB_API_KEY", default="")
EMAIL = config("EMAIL", default="")
PASSWORD = config("PASSWORD", default="")


def find_my_ip():
    ip_address = requests.get('https://api64.ipify.org?format=json').json()
    return ip_address["ip"]


def search_on_wikipedia(query):
    results = wikipedia.summary(query, sentences=2)
    return results


def play_on_youtube(video):
    if kit:
        try:
            kit.playonyt(video)
            return
        except Exception:
            pass
    webbrowser.open(f"https://www.youtube.com/results?search_query={video}")


def search_on_google(query):
    if kit:
        try:
            kit.search(query)
            return
        except Exception:
            pass
    webbrowser.open(f"https://www.google.com/search?q={query}")


def send_whatsapp_message(number, message):
    if kit:
        try:
            kit.sendwhatmsg_instantly(f"+91{number}", message)
            return
        except Exception:
            pass
    webbrowser.open(f"https://web.whatsapp.com/send?phone=91{number}&text={message}")


def send_email(receiver_address, subject, message):
    try:
        email = EmailMessage()
        email['To'] = receiver_address
        email["Subject"] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False


def get_latest_news():
    if not NEWS_API_KEY or NEWS_API_KEY == "None":
        return ["News API key not configured. Please add NEWS_API_KEY to your .env file."]
    try:
        news_headlines = []
        res = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}&category=general").json()
        articles = res.get("articles", [])
        for article in articles:
            news_headlines.append(article["title"])
        return news_headlines[:5] if news_headlines else ["No news articles found."]
    except Exception as e:
        return [f"Could not fetch news: {e}"]


def get_weather_report(city):
    if not OPENWEATHER_APP_ID or OPENWEATHER_APP_ID == "None":
        return "Unknown", "N/A", "N/A (Please set OPENWEATHER_APP_ID in .env)"
    try:
        res = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
        if res.get("cod") != 200:
            return res.get("message", "Error"), "N/A", "N/A"
        weather = res["weather"][0]["main"]
        temperature = res["main"]["temp"]
        feels_like = res["main"]["feels_like"]
        return weather, f"{temperature}℃", f"{feels_like}℃"
    except Exception as e:
        return f"Error ({e})", "N/A", "N/A"


def get_trending_movies():
    if not TMDB_API_KEY or TMDB_API_KEY == "None":
        return ["TMDB API key not configured. Please add TMDB_API_KEY to your .env file."]
    try:
        trending_movies = []
        res = requests.get(
            f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
        results = res.get("results", [])
        for r in results:
            trending_movies.append(r["original_title"])
        return trending_movies[:5] if trending_movies else ["No trending movies found."]
    except Exception as e:
        return [f"Could not fetch trending movies: {e}"]


def get_random_joke():
    headers = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return res["joke"]


def get_random_advice():
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']
