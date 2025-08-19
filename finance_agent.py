from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools
from agno.tools.duckduckgo import DuckDuckGoTools

def build_agent(api_key: str):
    """Build and return a finance agent with the provided API key"""
    if not api_key or not api_key.strip():
        raise ValueError("API key is required to create the finance agent.")
    
    return Agent(
        model=Groq(id="llama-3.3-70b-versatile", api_key=api_key),
        tools=[YFinanceTools(), DuckDuckGoTools()],
        instructions=(
            "You are a professional finance assistant. "
            "Provide clear, accurate financial information with proper formatting. "
            "Use bullet points for key information, tables when appropriate, "
            "and always cite your sources. Be helpful and informative."
        ),
        show_tool_calls=True,
        markdown=True
    )

def get_agent(api_key: str):
    """Create and return agent instance with the provided API key"""
    return build_agent(api_key)

if __name__ == "__main__":
    # Test the agent
    test_agent = get_agent()
    response = test_agent.run("What is the current price of Apple stock?")
    print(response)