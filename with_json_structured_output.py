from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from typing import Literal 

model = ChatOpenAI(model="gpt-4o")
# schema
review = {
    "title":"Review",
    "description":"schema about a review",
    "type": "object",
    "properties":{
        "summary":{
            "type":"string",
            "description":"summary of the review"
        },
        "sentiment":{
            "type":"string",
            "description":"sentiment of the review",
            "enum":["pos","neg"]
        },
        "theme":{
            "type":"array",
            "items":{
                "type":"string"
            },
            "description":"write down all the key themes discussed in reveiew"
        }
    },
    "required":["summary","sentiment","theme"]
}

structure_output = model.with_structured_output(review)
result = structure_output.invoke("""The hardware is great but the software is bloated.
                       Already
                       1. It takes a long time to boot up.
                       2. It has a lot of pre-installed apps that I never use.
                       3. The user interface is cluttered and hard to navigate.
                       4. It has a lot of background processes that slow down the performance.
                       5. It has a lot of bugs and crashes frequently.
                       6. It has a lot of unnecessary features that I never use.""")

print(result)