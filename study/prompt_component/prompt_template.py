from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from datetime import datetime

prompt = PromptTemplate.from_template("请讲一个关于{subject}的冷笑话！")
print(prompt.format(subject="喜剧演员"))
prompt_value = prompt.invoke({"subject": "喜剧演员"})
print(prompt_value.to_string())
print(prompt_value.to_messages())

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是OpenAI开发的聊天机器人，请根据用户的提问进行回复，当前的时间为：{now}"),
    MessagesPlaceholder("chat_history"), 
    HumanMessagePromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
]).partial(now=datetime.now())
 
chat_prompt_value = chat_prompt.invoke({"chat_history": [],"subject": "程序员"})  

print(chat_prompt_value)
print(chat_prompt_value.to_string())
