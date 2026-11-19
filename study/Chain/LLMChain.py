import dotenv

from langchain.chains.llm import LLMChain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(model="deepseek-v4-pro",temperature=0.5,max_tokens=1024)

chain = LLMChain(llm=llm, prompt=prompt)