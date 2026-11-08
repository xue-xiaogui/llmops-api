import dotenv
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

dotenv.load_dotenv()

def retrieval(query: str) ->str:
    """一个模拟的检索器函数"""
    print("正在检索:", query)
    return "我是慕小课"

# 1. 编排promat
prompt = ChatPromptTemplate.from_template("""请根据用户的问题回答，可以参考对应的上下文进行生成。
<context>{context}</context>
用户提问的问题：{query}    
""")

# 创建大语言模型
llm = ChatOpenAI(model="deepseek-v4-pro",temperature=0.5,max_tokens=1024)

# 创建输出解析器
parser = StrOutputParser()

chain_one = {
    "context": retrieval,
    "query": RunnablePassthrough()
} | prompt | llm | parser 

chain_two = RunnablePassthrough.assign({
    "context": lambda x: retrieval(x["query"]),
    "query": RunnablePassthrough()
}) | prompt | llm | parser 

result_one = chain_one.invoke("动物")
result_two = chain_two.invoke({"query": "动物"}) 

print(result)