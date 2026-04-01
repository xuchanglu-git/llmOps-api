#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
对比 LangChain 和原生 OpenAI SDK 的流式输出方式
"""
import time
from openai import OpenAI

client = OpenAI(
    api_key="sk-r1dmsG2q5wO2WmXYeNxoaJBkDiiS2Tm3UHQBtprC4JSdUWXT",
    base_url="https://api.moonshot.cn/v1",
)

response = client.chat.completions.create(
    model="kimi-k2.5",
    messages=[
        {
            "role": "system",
            "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。",
        },
        {"role": "user", "content": "你好，我叫李雷， 生成50英文短文"},
    ],
    stream=True,
)

collected_messages = []
for idx, chunk in enumerate(response):
    chunk_message = chunk.choices[0].delta
    if not chunk_message.content:
        continue
    collected_messages.append(chunk_message)  # save the message
    print(f"#{idx}: {''.join([m.content for m in collected_messages])}")
print(f"Full conversation received: {''.join([m.content for m in collected_messages])}")