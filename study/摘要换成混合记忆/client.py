from calendar import c
from typing import Any

import dotenv
import os

from httpx2 import query
from openai import OpenAI

dotenv.load_dotenv()

# 1. max_tokens 用于判断是否需要生成新的摘要
# 2. summary 用于存储摘要的信息
# 3. chat_histories 用于存储历史对话
# 4. get_num_tokens 用于计算传入文本的 token 数
# 5. save_context 用于存储新的交流对话
# 6. get_buffer_string 用于将历史对话转换成字符串
# 7. load_memory_variables 用于加载记忆变量信息
# 8. summary_text 用于将旧的摘要和传入的对话生成新的摘要
class ConversationsummaryBufferMemory:
    def __init__(self, summary: str = '', chat_history: list = None ,max_tokens: int = 300):
        self.max_tokens = max_tokens
        self.summary = summary
        self.chat_history = [] if chat_history is None else chat_history
        self._client= OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE"),
        )
    
    # 用于技术传入文本的token数
    @classmethod
    def get_num_tokens(cls, text: str) -> int:  
        return len(text)

    # 用于存储新的交流对话
    def save_context(self, human_query: str, ai_content: str) -> None:
        self.chat_history.append({"human": human_query, "ai": ai_content})
        buffer_string = self.get_buffer_string()
        tokens = self.get_num_tokens(buffer_string)
        if tokens > self.max_tokens:
            first_chat = self.chat_history[0]
            print("新摘要生成中~")
            self.summary = self.summary_text(self.summary, f"Human:{first_chat.get('human')}\nAI:{first_chat.get('ai')}")
            print("新摘要生成成功：", self.summary)
            del self.chat_history[0]        

    # 用于将历史对话转换成字符串
    def get_buffer_string(self) -> str:
        buffer: str = ""
        for chat in self.chat_history:
            buffer += f"Human:{chat.get('human')}\nAI:{chat.get('ai')}\n\n"
        
        return buffer 

    # 用于加载记忆变量信息
    def load_memory_variables(self) -> dict[str, Any]:
        buffer_string = self.get_buffer_string()
        return {"chat_history": f"摘要：{self.summary}\n\n历史信息：{buffer_string}\n"}

    # 用于将旧的摘要和传入的对话生成新摘要
    def summary_text(self, origin_summary: str, new_line: str) -> str:
        prompt = f"""
            你是一名专业的信息摘要助手。

            请阅读以下内容，提取核心信息，
            生成准确、简洁、结构化的摘要。

            原始摘要：{origin_summary}

            要求：
            1. 不得编造原文没有的信息。
            2. 保留重要事实和关键结论。
            3. 删除重复和冗余内容。
            4. 使用清晰的标题和列表。

            新的对话： 
            {new_line}
        """
        
        return self._client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=[
                {"role": "user", "content": prompt},
            ],
            temperature=0.5, 
            max_tokens=self.max_tokens,
            stream=False,
        ).choices[0].message.content

    # 1.max_tokens 用于判断是否需要生成新的摘要
    # 2.summary 用于存储摘要的信息
    # 3.chat_history 用于存储对话历史
    
    pass



# 创建OpenAI客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_API_BASE"),
)
memory = ConversationsummaryBufferMemory("", [], max_tokens=300)

# 创建一个死循环用于人机对话
while True:
    # 1.获取用户输入
    query = input("Human：")
    # 2.判断用户输入是否是退出
    if query == "q":
        break

    memory_variables = memory.load_memory_variables()
    answer_prompt = (
        "你是一个强大的聊天机器人，请根据对应的上下文和用户提问解决问题。\n\n"
        f"{memory_variables.get('chat_history', '')}\n"
        f"用户的提问时：{query}"  
    )

    # 3.调用OpenAI API获取模型回复
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "user", "content": answer_prompt}
        ],
        temperature=0.5, 
        stream=True,    
    )
    # 4.打印模型回复
    print("AI：", flush=True, end="")
    ai_content = ""
    for chunk in response:
        if not chunk.choices:
            continue

        content = chunk.choices[0].delta.content

        if content is None:
            continue
        
        ai_content += content
        print(content, flush=True, end="")
    memory.save_context(query, ai_content)
    