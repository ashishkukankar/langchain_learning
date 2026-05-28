from dotenv import load_dotenv
from ollama import Tool

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain.tools import tool
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


# ------Agent Loop------

def run_agent(question:str):
    tools =[get_product_price,get_product_discount]
    tool_dic = {t.name: t for t in tools}
    llm = init_chat_model(f"ollama:{MODEL}", temerature=0)
    bind_tools_llm = llm.bind_tools(tools)

    print(f"Question: {question}")
    print("="* 60)

    messages = [
        SystemMessage(
            content = (
                "You are a helpful assistant for answering product price questions."
                "You have access to product catalog tools"
                "and a discount tool.\n\n "
                "Strict rules: YOu must follow this exact rules\n"
                "1. Never guess or assume product price"
                "You must call the get product price first to get product real price.\n"
                "2. Only call the get product discount after you have received"
                "the real price from get product price tool.\n"
                "3. Never calculate the discount price by youself using Math"
                "and always call the get product discount tool. \n"
                "4. IF use does not give discount type, then ask the user to choose discount type from gold, silver and platinum. \n"

            )
        ),
        HumanMessage(content=question)
    ]

    for i in range(MAX_ITERATIONS +1):
        print(f"_______Iteration {i}_______")
        """
        Agent thought process. On the basis of the messages, agent decide to call tool 
        as per the messages
        """ 
        ai_message = bind_tools_llm.invoke(messages)
        tools_call = ai_message.tool_calls
        """
        Ageent verify the message and check any tool is available 
        and if not then return the result to user
        """ 
        if not tools_call:
            print("Agent's answer: ", ai_message.content)
            return ai_message.content
        """
        invoking the tools
        """ 
        tool_call = tools_call[0]
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args")
        tool_call_id = tool_call.get("id")

        tool_to_user = tool_dic.get(tool_name)

        if not tool_to_user:
            print(f"Tool {tool_name} not found.")
            return
        
        observation = tool_to_user.invoke(tool_args)

        print(f" Observation : {observation}")

        """
        Appending the ai_message and tool observation to the messages for next iteration
        """ 
        messages.append(ai_message)
        messages.append(ToolMessage(content=observation, tool_call_id=tool_call_id ))
        

        

        

if __name__ == "__main__":
    print("Hello Langchain Agtent(.bind_tools)")
    print()
    result = run_agent("What is the price of laptop with gold discount?")
