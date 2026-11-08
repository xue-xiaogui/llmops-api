import uuid

import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.callbacks import StreamingStdOutCallbackHandler, BaseCallbackHandler
from langchain_core.messages import BaseMessage
from langchain_openai import ChatOpenAI

from typing import Any, Dict, List

dotenv.load_dotenv()

class LLMopsCallbackHandler(BaseCallbackHandler):
    """ 自定义LLMOps回调处理器 """
    def on_chat_model_start(
        self,
        serialized: dict[str, Any],
        messages: list[list[BaseMessage]],
        *,
        run_id: str,
        parent_run_id: str,
        tags: list[str],
        metadata: dict[str, Any],
        **kwargs: Any
    ):
        print(f"LLM 开始运行: {run_id}, {serialized}, {messages}")  

    def on_chat_model_end(
        self,
        response: LLMResult,
        *,
        run_id: uuid.UUID,
        parent_run_id: uuid.UUID,
        **kwargs: Any
    ):
        print(f"LLM 运行结束: {run_id}, {response}, {messages}")  
    
    # def on_chat_new_token(
    #     self,
    #     serialized: dict[str, Any],
    #     token: str,
    #     *,
    #     run_id: str,
    #     parent_run_id: str,
    #     tags: list[str],
    #     metadata: dict[str, Any],
    #     **kwargs: Any
    # ):
    #     print(f"LLM 新token: {run_id}, {serialized}, {token}")  

# 1.编排prompt
prompt = ChatPromptTemplate.from_template("{query}")

# 2.编排llm
llm = ChatOpenAI(model="deepseek-v4-pro",temperature=0.5,max_tokens=1024)

# 3. 构建链
chain = {"query": RunnablePassthrough()} | prompt | llm | StrOutputParser()

# 4. 执行链
print(chain.invoke("你好，你是？", config={"callbacks": [StreamingStdOutCallbackHandler(), LLMopsCallbackHandler()]}))
 