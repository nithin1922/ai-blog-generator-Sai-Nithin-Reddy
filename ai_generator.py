import os
from groq import Groq
from dotenv import load_dotenv
from seo_fetcher import get_metrics
from langgraph.graph import StateGraph, END
from langgraph.prebuilt.tool_node import ToolNode
from typing import TypedDict, Optional
load_dotenv()

# Initialize Groq client using the GROQ_API_KEY environment variable
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def blog_post_prompt(keyword: str, seo: dict) -> str:
    return (
        f"Write a detailed blog post draft about '{keyword}'. "
        f"Include an introduction, 3–5 subheadings with content, and a conclusion. "
        f"Embed three placeholder affiliate links as {{AFF_LINK_1}}, {{AFF_LINK_2}}, {{AFF_LINK_3}}. "
        f"Also mention the following SEO stats: "
        f"search volume is {seo['search_volume']}, keyword difficulty is {seo['keyword_difficulty']}, "
        f"and average CPC is ${seo['avg_cpc']}.")

# Tool to fetch SEO metrics
def fetch_seo_tool(input: dict) -> dict:
    """
    Fetch SEO metrics for a given keyword.
    Expects input: {'keyword': str}
    Returns: {'keyword': str, 'seo': dict}
    """
    keyword = input["keyword"]
    seo = get_metrics(keyword)
    return {"keyword": keyword, "seo": seo}

# Tool to generate blog post using Groq LLM
def groq_blog_post_tool(input: dict) -> dict:
    """
    Generate a blog post draft using Groq LLM.
    Expects input: {'keyword': str, 'seo': dict}
    Returns: {'post': str}
    """
    keyword = input["keyword"]
    seo = input["seo"]
    prompt = blog_post_prompt(keyword, seo)
    response = client.chat.completions.create(
        model='llama3-8b-8192',
        messages=[
            {'role': 'system', 'content': 'You are a helpful blogging assistant.'},
            {'role': 'user', 'content': prompt}
        ]
    )
    return {"post": response.choices[0].message.content or ""}

# Tool to write blog post to a markdown file
def write_markdown_tool(input: dict) -> dict:
    """
    Write the generated blog post to a markdown file.
    Expects input: {'keyword': str, 'post': str}
    Returns: {'filepath': str}
    """
    keyword = input["keyword"].replace(" ", "_").lower()
    post = input["post"]
    filename = f"daily_{keyword}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(post)
    return {"filepath": filename, **input}

# Define the state schema for LangGraph
class BlogGenState(TypedDict, total=False):
    keyword: str
    seo: dict
    post: str
    filepath: str

# Define LangGraph agent
def generate_post_with_agent(keyword: str):
    # Build the graph
    graph = StateGraph(state_schema=BlogGenState)
    graph.add_node("fetch_seo", fetch_seo_tool)
    graph.add_node("generate_blog", groq_blog_post_tool)
    graph.add_node("write_markdown", write_markdown_tool)
    graph.add_edge("fetch_seo", "generate_blog")
    graph.add_edge("generate_blog", "write_markdown")
    graph.add_edge("write_markdown", END)
    graph.set_entry_point("fetch_seo")

    # Run the agent
    state = {"keyword": keyword}
    compiled_graph = graph.compile()
    result = compiled_graph.invoke(state)
    return result["post"], result["seo"], result["filepath"]