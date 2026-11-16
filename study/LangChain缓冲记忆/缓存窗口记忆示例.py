from operator import itemgetter

import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferWindowMemory, ConversationBufferMemory
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

dotenv.load_dotenv()

# 1. 创建提示模版
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAI开发的聊天机器人，请根据用户的提问进行回复"),
    MessagesPlaceholder("history"),
    ("human", "{query}"),
])

# 1. 定义缓存窗口记忆
memory = ConversationBufferWindowMemory(
    k=2,
    return_messages=True,
    input_key="query",
    memory_key="history",
    output_key="output"
)
  
# 2. 定义模型
llm = ChatOpenAI(model="deepseek-v4-pro",temperature=0.5,max_tokens=1024)

# 3. 构建链
chain = (
    RunnablePassthrough.assign(
        history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
    )
    | prompt
    | llm
    | StrOutputParser()
)

# 4. 死循环构建对话命令行
while True:
    query = input("Human：")

    if query == "q":
        exit(0)
          
    chain_input = {"query": query, "language": "中文"}

    response = chain.stream(chain_input)
    output = ""
    for chunk in response:
        output += chunk
        print(chunk, flush=True, end="")
    memory.save_context(chain_input, {"output": output})
    print("")
