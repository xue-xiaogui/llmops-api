import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.chat_message_histories import FileChatMessageHistory    

dotenv.load_dotenv()

store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = FileChatMessageHistory(f"./chat_history_{session_id}.txt")
    return store[session_id]

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的翻译"),
    ("human", "{input}"),
])

llm = ChatOpenAI(model="deepseek-v4-pro",temperature=0.5,max_tokens=1024)

# 定义链
chain = prompt | llm | StrOutputParser()


# 包装链 
with_message_chain = RunnableWithMessageHistory(chain, get_session_history, input_messages_key="query", history_messages_key="history")   

while True:
    query = input("请输入: ")
    if query == "q":
        break

    response = with_message_chain.stream({"query": query}, {"config": {"configurable": {"session_id": "慕小课"}}})
    print("AI", flush="", end="")
    for chunk in response:
        print(chunk, flush=True, end="") 
