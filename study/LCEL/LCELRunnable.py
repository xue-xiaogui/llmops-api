import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


dotenv.load_dotenv()   

# 构建组件
prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(model="deepseek-v4-pro",temperature=0.5,max_tokens=1024)
parser = StrOutputParser()

# 编排链
chain = prompt | llm | parser

# 执行链
print(chain.invoke({"query": "你好，你是？"}))