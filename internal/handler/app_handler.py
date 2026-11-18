from operator import itemgetter
from internal.schema.app_schema import CompletionReq
from pkg.response import success_json, validate_error_json, success_message
from internal.exception import FailException
from internal.service import AppService, app_service
from injector import inject
from dataclasses import dataclass
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import FileChatMessageHistory

import os
from uuid import UUID
# 应用处理模块  
@inject
@dataclass
class AppHandler:

    # 应用控制器
    app_service: AppService = app_service

    def create_app(self):
        # 调用服务创建新的APP记录
        app = self.app_service.create_app()
        return success_message(f"创建AI应用成功，应用ID为：{app.id}")

    def get_app(self, id: UUID):
        app = self.app_service.get_app(id)
        if not app:
            raise FailException(f"应用ID为：{id}的AI应用不存在")
        return success_message(f"获取AI应用成功，应用名称为：{app.name}")

    def update_app(self, id: UUID):
        app = self.app_service.update_app(id)
        return success_message(f"更新AI应用成功，应用名称为：{app.name}")

    def delete_app(self, id: UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"删除AI应用成功，应用ID为：{app.id}")
        
    def debug(self, app_id: UUID):
        # 1.提取从接口中获取的输入
        req = CompletionReq()
        if not req.validate(): 
            return validate_error_json(req.errors)

        prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个强大的聊天机器人，能解决用户的任何问题"),
            MessagesPlaceholder("history"),
            ("human", "{query}"),
        ])

        store = FileChatMessageHistory("./storage/chat_history.txt")

        def load_history(_):
            # 保留最近 3 轮对话（共 6 条消息）
            return {"chat_history": store.messages[-6:]}

        llm = ChatOpenAI(model="deepseek-v4-pro",temperature=0.5,max_tokens=1024)

        # 创建langchain链
        chain = RunnablePassthrough.assign(
            history=RunnableLambda(load_history) | itemgetter("chat_history"),
        ) | prompt | llm | StrOutputParser()

        # 调用langchain链
        chain_input = {"query": req.query.data}
        content = chain.invoke(chain_input)
        store.add_message(HumanMessage(content=req.query.data))
        store.add_message(AIMessage(content=content))

        return success_json({"content": content})
         
    def ping(self):
        raise FailException("数据未找到")
        #    return success_json({"ping": "ok"})

