import random

def get_metrics(keyword: str):
    # Mocked SEO metrics
    return {
        'search_volume': random.randint(500, 5000),
        'keyword_difficulty': round(random.uniform(10, 90), 2),
        'avg_cpc': round(random.uniform(0.2, 5.0), 2)
    }