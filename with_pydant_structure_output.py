from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from typing import Literal 

model = ChatOpenAI(model="gpt-4o")
# schema
class Review(BaseModel):
    summary:str = Field(description="summary of the review")
    sentiment:Literal["pos","neg"] = Field(description="sentiment of the review")
    theme:list[str] = Field(description="write down all the key themes discussed in reveiew")

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