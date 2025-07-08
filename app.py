import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from seo_fetcher import get_metrics
from ai_generator import generate_post_with_agent

# Load environment
load_dotenv()

app = Flask(__name__)

@app.route('/generate')
def generate():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Keyword parameter is required'}), 400

    # Generate post draft and SEO metrics using LangGraph agent
    post, seo, filepath = generate_post_with_agent(keyword)

    return jsonify({'keyword': keyword, 'seo': seo, 'post': post, 'filepath': filepath})

if __name__ == '__main__':
    # Run Flask
    app.run(host='0.0.0.0', port=5000)