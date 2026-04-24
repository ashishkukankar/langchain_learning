## Structure Output

https://docs.langchain.com/oss/python/langchain/structured-output

Structure outputs allow agent to return output in specific, predicted formate instead of plain text. You will get structure output in form of json object, Pedantic Model, data classes which is used by your application directly.

Some llm provide which create structure output for example openAI 

**Format**

**TypedDict**: TypeDict is a way to define a dictionary in Python which specify what key and value should be exist
1. It tells in python what keys are required and what are their types
2. It does not validate data in runtime
3. we cann’t do data validation

**Pydantic**: Pydantic is data-validation and data-parsing library for python. It ensure the data you work is correct, structured and type-safe. It is very powerful library.
Uses field to add condition in the value

JASON: creat schema. We can define types for validation