from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_tavily import TavilySearch

llm = ChatOpenAI(model="gpt-3.5-turbo")
agent = create_agent(llm, tools=[TavilySearch()])

def main():
    result = agent.invoke({"messages": [("human", "Current AI skills needed for ai gen ")]})
    print(result["messages"][-1].content)  # Final LLM response

if __name__ == "__main__":
    main()