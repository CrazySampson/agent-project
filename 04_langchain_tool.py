import os
import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
# 关键修改：从 langchain_classic.agents 导入
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

# ... 其余代码保持不变 ...

# 加载 .env 中的 API Key
load_dotenv()

# ===== 1. 用 @tool 装饰器定义工具（告别手写 JSON Schema）=====
@tool
def get_current_time() -> str:
    """获取当前系统时间，返回格式为 YYYY-MM-DD HH:MM:SS。"""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ===== 2. 封装 DeepSeek 模型 =====
model = ChatOpenAI(
    model="deepseek-chat",          # 使用 DeepSeek 模型
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0.7
)

# ===== 3. 定义提示词模板 =====
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个有用的助手，可以调用工具获取信息。"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")      # 必须保留，Agent 用来自动记录中间步骤
])

# ===== 4. 创建工具调用的 Agent =====
tools = [get_current_time]                     # 工具列表
agent = create_tool_calling_agent(model, tools, prompt)

# ===== 5. 创建执行器（封装了工具调用的循环逻辑）=====
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,               # 打开后可看到内部思考过程
    handle_parsing_errors=True
)

# ===== 6. 运行对话循环 =====
print("🤖 LangChain Agent 已启动！输入 'quit' 退出。")

while True:
    user_input = input("\n你: ")
    if user_input.lower() == "quit":
        print("👋 再见！")
        break

    # 一行代码完成整个对话流程！
    response = agent_executor.invoke({"input": user_input})
    print(f"助手: {response['output']}")