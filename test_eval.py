import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")
from judgeval import JudgmentClient
from judgeval.data import Example
from judgeval.scorers import FaithfulnessScorer
from ai_generator import generate_post_with_agent

def test_blog_post_faithfulness():
    keyword = "wireless earbuds"
    post, seo, filepath = generate_post_with_agent(keyword)
    example = Example(
        input=keyword,
        actual_output=post,
        retrieval_context=[
            f"search volume: {seo['search_volume']}, keyword difficulty: {seo['keyword_difficulty']}, avg cpc: {seo['avg_cpc']}"
        ],
    )
    scorer = FaithfulnessScorer(threshold=0.5)
    client = JudgmentClient()
    print("Example:", example)
    print("Scorer:", scorer)
    print("Model:", "gpt-4.1")
    client.assert_test(
        examples=[example],
        scorers=[scorer],
        model="gpt-4.1",
    )

if __name__ == "__main__":
    test_blog_post_faithfulness()
    print("Eval test completed.") 