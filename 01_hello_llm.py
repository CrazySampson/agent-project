import os
from openai import OpenAI
from dotenv import load_dotenv

#加载.env文件中的环境变量
load_dotenv()

#初始化客户端（使用DeepSeek 的 API地址）
client=OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)

#调用聊天补全接口
response=client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role":"user","content":"用一句话介绍AI Agent"}
    ]
)

print(response.choices[0].message.content)