import json
import datetime
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

# ===== 1. 定义工具函数（真实的业务逻辑）=====
def get_current_time():
    """获取当前系统时间"""
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"time": current_time}

# ===== 2. 定义工具的 JSON Schema（告诉模型这个工具长什么样）=====
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前系统时间，返回格式为 YYYY-MM-DD HH:MM:SS",
            "parameters": {
                "type": "object",
                "properties": {},     # 该函数无需参数
                "required": []
            }
        }
    }
]

# ===== 3. 对话消息历史 =====
messages = [
    {"role": "system", "content": "你是一个有用的助手，可以调用工具获取信息。"}
]

print("🛠️ 工具调用演示启动！输入 'quit' 退出。")
print("试试问：现在几点了？")

while True:
    user_input = input("\n你: ")
    if user_input.lower() == "quit":
        print("👋 再见！")
        break

    # 将用户消息加入历史
    messages.append({"role": "user", "content": user_input})

    # ===== 4. 第一次调用模型（可能返回 tool_calls）=====
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools,           # 传递工具定义
        tool_choice="auto"     # 让模型自动决定是否调用工具
    )

    response_message = response.choices[0].message
    messages.append(response_message)   # 先把模型的响应追加到历史

    # ===== 5. 检查模型是否需要调用工具 =====
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            # 获取工具名称和参数
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            print(f"🔧 调用工具：{tool_name}，参数：{tool_args}")

            # 根据工具名称执行对应的函数
            if tool_name == "get_current_time":
                tool_result = get_current_time()
            else:
                tool_result = {"error": "未知工具"}

            # 将工具执行结果封装成消息，返回给模型
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result, ensure_ascii=False)
            })

        # ===== 6. 第二次调用模型（带上工具执行结果，生成最终答案）=====
        final_response = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages
        )
        final_answer = final_response.choices[0].message.content
        print("助手:", final_answer)
        messages.append({"role": "assistant", "content": final_answer})
    else:
        # 没有工具调用，直接输出普通回复
        print("助手:", response_message.content)
