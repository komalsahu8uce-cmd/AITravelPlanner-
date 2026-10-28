import os

from tavily import TavilyClient


def load_dotenv(dotenv_path=".env"):
    """Load environment variables from a .env file without requiring python-dotenv."""
    if not os.path.exists(dotenv_path):
        return False

    with open(dotenv_path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)

    return True


load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
client = TavilyClient(api_key=api_key) if api_key else None


def tavily_search(query):
    if client is None:
        return (
            "Tavily is not configured. Set the TAVILY_API_KEY environment variable "
            "or add it to your .env file to enable live web search."
        )

    response = client.search(query=query, max_results=5)

    results = []

    for i, r in enumerate(response["results"], 1):
        title = r.get("title", "Unknown")
        url = r.get("url", "")
        snippet = r.get("content", "").strip()
        # Keep only the first 300 characters to avoid wall-of-text
        if len(snippet) > 300:
            snippet = snippet[:300].rsplit(" ", 1)[0] + "..."

        results.append(f"{i}. **{title}**\n   {url}\n   {snippet}")

    return "\n\n".join(results)