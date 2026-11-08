import dotenv
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAI

dotenv.load_dotenv()

# 1. 定义提示模板prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAI开发的聊天机器人，请根据用户的提问进行回复，当前的时间为：{now}"),
    ("human", "{query}")
]).partial(now=datetime.now())

# 2. 定义模型
llm = ChatOpenAI(model="deepseek-v4-pro",temperature=0.5,max_tokens=1024)

# 3. 调用模型
# response = llm.invoke(prompt.invoke({"query": "现在是几点，请讲一个程序员的冷笑话"}))
# # print(response)
# print(response.content) 

# 批量调用模型
responses = llm.stream(prompt.invoke({"query": "现在是几点，请讲一个程序员的冷笑话"}))
print(responses)
for chunk in responses:
    print(chunk.content, flush=True, end="")
