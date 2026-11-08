import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser


dotenv.load_dotenv()   

# 构建组件
prompt = ChatPromptTemplate.from_template("{query}")
llm = ChatOpenAI(model="deepseek-v4-pro",temperature=0.5,max_tokens=1024)
parser = StrOutputParser()

# 定义链
class Chain:
    steps:list = []
    def __init__(self, steps:list):
        self.steps = steps

    def invoke(self, input:Any):
        for step in self.steps:
            input = step.invoke(input)
        return input

# 编排链
chain = Chain([prompt, llm, parser])
# 执行链
print(chain.invoke({"query": "你好，你是？"})) 