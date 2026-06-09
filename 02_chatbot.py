import os
from openai import OpenAI
from dotenv import load_dotenv
from colorama import Fore,Style,init
import json
load_dotenv()
init(autoreset=True) #自动重置颜色

# 初始化客户端（使用DeepSeek 的 API地址）
client=OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1"
)


print("请选择助手角色：1. 普通助手  2. 程序员  3. 诗人")
choice = input("输入数字: ")
if choice == "2":
    system_prompt = "你是一名经验丰富的程序员，回答时尽量给出代码示例。"
elif choice == "3":
    system_prompt = "你是一位浪漫的诗人，每句话都富有诗意。"
else:
    system_prompt = "你是一个有用的助手。"
messages = [{"role": "system", "content": system_prompt}]

print("聊天机器人已启动，输入'quit'结束对话。")

#主循环：不断接收用户输入

while True:
    user_input = input(f"{Fore.GREEN}你: {Style.RESET_ALL}")
    if user_input.lower()=="quit":
        print("再见！")
        break

    #将用户输入添加到消息列表
    messages.append({"role":"user","content":user_input})

    #调用API并开启流式输出
    stream=client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=True         #关键参数
    )

    print(f"{Fore.BLUE}助手: ", end="", flush=True) #不换行，实时打印
    full_reply="" #用于存储完整回复
    for chunk in stream:
        if chunk.choices[0].delta.content:
            text=chunk.choices[0].delta.content
            print(text, end="", flush=True) #逐字打印
            full_reply+=text
    print() #换行


    #将助手的完整回复也加入历史，以便下一轮记住上下文
    messages.append({"role":"assistant","content":full_reply})

with open("chat_history.json", "w", encoding="utf-8") as f:
    json.dump(messages, f, ensure_ascii=False, indent=2)
print("对话已保存到 chat_history.json")