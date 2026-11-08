import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_template("{query}")

llm = ChatOpenAI(model="deepseek-v4-pro",temperature=0.5,max_tokens=1024)

parser = StrOutputParser()

result = parser.invoke(llm.invoke(prompt.invoke({"query": "你好，你是？"})))
print(result)