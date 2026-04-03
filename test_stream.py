#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试流式输出效果"""
import time
from openai import OpenAI

client = OpenAI(
    api_key="sk-r1dmsG2q5wO2WmXYeNxoaJBkDiiS2Tm3UHQBtprC4JSdUWXT",
    base_url="https://api.moonshot.cn/v1",
)

print("开始发起流式请求...")
start_time = time.time()

response = client.chat.completions.create(
    model="kimi-k2.5",
    messages=[
        {"role": "user", "content": "请详细介绍一下你自己"},
    ],
    stream=True,
)

print("\n=== AI 回答开始 ===\n")
print("AI: ", end="", flush=True)

chunk_count = 0
total_time = 0
first_chunk_time = None

for chunk in response:
    current_time = time.time()
    
    if chunk.choices and len(chunk.choices) > 0:
        content = chunk.choices[0].delta.content
        
        if content is not None:
            chunk_count += 1
            
            # 记录第一个内容块的时间
            if first_chunk_time is None:
                first_chunk_time = current_time
                print(f"\n[收到第 1 个 chunk，耗时：{current_time - start_time:.3f}s]\n")
            
            # 打印内容和时间戳
            elapsed = current_time - start_time
            print(f"[{elapsed:.3f}s] {repr(content)} -> {content}", end="", flush=True)
            
            # 添加小延迟以便观察流式效果（可选）
            # time.sleep(0.05)

print("\n\n=== AI 回答结束 ===")
print(f"\n总共收到 {chunk_count} 个 chunk")
print(f"总耗时：{time.time() - start_time:.3f}s")
