# AI Blog Generator

This project is an AI-powered blog post generator that uses SEO metrics and Groq LLM to create detailed blog drafts on any keyword. It features a Flask API endpoint for generating posts, and saves the output as markdown files.

## Features
- Fetches SEO metrics for a given keyword (mocked for demo)
- Generates a detailed blog post draft using Groq LLM
- Saves the generated post as a markdown file
- Exposes a `/generate` API endpoint for easy integration

## Requirements
- Python 3.8+
- See `requirements.txt` for Python dependencies

## Installation
1. Clone this repository:
   ```bash
   git clone <repo-url>
   cd ai-blog-generator-interview-Sai-Nithin-Reddy
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment variables:
   - Create a `.env` file in the project root with your Groq API key:
     ```env
     GROQ_API_KEY=your_groq_api_key_here
     ```

## Usage
Run the Flask app:
```bash
python app.py
```

The API will be available at `http://localhost:5000/generate?keyword=YOUR_KEYWORD`.

### Example Request
```
GET /generate?keyword=wireless earbuds
```

### Example Response
```json
{
  "keyword": "wireless earbuds",
  "seo": {
    "search_volume": 3806,
    "keyword_difficulty": 58.97,
    "avg_cpc": 2.26
  },
  "post": "...generated blog post...",
  "filepath": "daily_wireless_earbuds.md"
}
```

## File Overview
- `app.py`: Flask API exposing the `/generate` endpoint.
- `ai_generator.py`: Core logic for fetching SEO, generating blog post, and saving markdown.
- `seo_fetcher.py`: Mocked SEO metrics fetcher.
- `requirements.txt`: Python dependencies.

## Environment Variables
- `GROQ_API_KEY`: Your Groq API key (required for LLM generation).

## Notes
- SEO metrics are mocked for demonstration purposes.
- The generated markdown files are saved as `daily_<keyword>.md` in the project root.

## License
MIT (or specify your license) 