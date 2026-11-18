from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_community.chat_message_histories import PostgresChatMessageHistory

chat_history = InMemoryChatMessageHistory()

chat_history.add_user_message("你好,我是慕小课，你是谁？")
chat_history.add_ai_message("我是慕小课，你是一个智能助手") 

print(chat_history.messages)