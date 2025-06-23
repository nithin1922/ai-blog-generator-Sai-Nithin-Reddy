import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from seo_fetcher import get_metrics
from ai_generator import generate_post

# Load environment
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/generate')
def generate():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Keyword parameter is required'}), 400

    # Fetch SEO metrics
    seo = get_metrics(keyword)

    # Generate post draft
    post = generate_post(keyword, seo)

    return jsonify({'keyword': keyword, 'seo': seo, 'post': post})


def daily_job():
    keyword = 'wireless earbuds'
    seo = get_metrics(keyword)
    post = generate_post(keyword, seo)
    filename = f"daily_{keyword.replace(' ', '_')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(post)
    print(f"Generated and saved: {filename}")


if __name__ == '__main__':
    # Scheduler setup
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_job, 'interval', days=1)
    scheduler.start()

    # Run Flask
    app.run(host='0.0.0.0', port=5000)