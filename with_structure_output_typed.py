from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from typing import TypedDict,Annotated

model = ChatOpenAI(model="gpt-4o")

# define schema for the output
class Review(TypedDict):
    summary:Annotated[str,"summary of the product review within 50 words"]
    sentiment:Annotated[str,"sentiment of the review- positive, negative or neutral"]

structure_output = model.with_structured_output(Review)

result = structure_output.invoke("""The hardware is great but the software is bloated.
                       Already
                       1. It takes a long time to boot up.
                       2. It has a lot of pre-installed apps that I never use.
                       3. The user interface is cluttered and hard to navigate.
                       4. It has a lot of background processes that slow down the performance.
                       5. It has a lot of bugs and crashes frequently.
                       6. It has a lot of unnecessary features that I never use.""")

print(result)