from dotenv import load_dotenv
from ollama import Tool
from langchain_core.prompts import  PromptTemplate

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_classic.tools import tool
from langchain_classic.agents import create_react_agent,AgentExecutor 
"""
using langchain_classic because these two methods
get Deprecated in latest langchain version but to 
understand the agent loop with prompt template, using it
 """
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

MAX_ITERATIONS = 10
MODEL ='qwen3:0.6b'

# ------Tools Definition------

@tool
def get_product_price(product: str)->float:
    '''Look up the price of a product in catalog.'''
    print(f" execute get_product_price(product:'{product}')")
    price ={"laptop":1800, "phone":29000, "earphone":2000}
    return price.get(product,0)


@tool
def get_product_discount(price:float, discount:str)->float:
    '''Apply a discount tier to the price and return the discounted price.
    Discount tier: gold, silver, platinum'''
    print(f" execute the get_product_discount(price:'{price}',discount:'{discount}')")
    discount_tier = {"gold":5, "silver":10, "platinum":20}
    discount = discount_tier.get(discount,0)
    return round(price* (1-discount/100),2)


tools = [get_product_price,get_product_discount]

template ="""
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""
        
prompt = PromptTemplate.from_template(template)

llm = init_chat_model(f"ollama:{MODEL}", temperature=0)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent = agent, tools = tools, verbose=True, handling_parsing_errors=True, max_iterations=MAX_ITERATIONS)

if __name__ == "__main__":
    print("Hello Langchain Agtent(.bind_tools)")
    print()
    result = agent_executor.invoke({"input": "What is the price of laptop with gold discount?"})
    print(result)
