import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel

dotenv.load_dotenv()

# 1. 编排promat
joke_prompt = ChatPromptTemplate.from_template("请讲一个关于{subject}的冷笑话")
poem_promprt = ChatPromptTemplate.from_template("请写一篇关于{subject}的诗")

# 创建大语言模型
llm = ChatOpenAI(model="deepseek-v4-pro",temperature=0.5,max_tokens=1024)

# 创建输出解析器
parser = StrOutputParser()

# 2. 构建链
joke_chain = joke_prompt | llm | parser
poem_chain = poem_promprt | llm | parser

# 3. 构建并行链
map_chain = RunnableParallel({
    "joke": joke_chain,
    "poem": poem_chain,
})