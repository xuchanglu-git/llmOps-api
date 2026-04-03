#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openai import OpenAI

client = OpenAI(
    api_key="sk-r1dmsG2q5wO2WmXYeNxoaJBkDiiS2Tm3UHQBtprC4JSdUWXT",
    base_url="https://api.moonshot.cn/v1",
)

print("正在发起请求...")
response = client.chat.completions.create(
    model="kimi-k2.5",
    messages=[
        {"role": "user", "content": "你好，测试一下"},
    ],
    stream=True,
)

print("开始读取响应...")
for i, chunk in enumerate(response):
    print(f"Chunk {i}: {chunk}")
    if chunk.choices and len(chunk.choices) > 0:
        content = chunk.choices[0].delta.content
        print(f"Content: {content}")
        if content:
            print(content, end="", flush=True)

print("\n完成！")
