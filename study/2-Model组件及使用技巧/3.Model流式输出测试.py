#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试流式输出效果
"""
import time
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    api_key='sk-r1dmsG2q5wO2WmXYeNxoaJBkDiiS2Tm3UHQBtprC4JSdUWXT',
    base_url='https://api.moonshot.cn/v1',
    model='kimi-k2.5'
)

print('开始流式输出测试（长文本）：')
print('=' * 60)
print()

start_time = time.time()

try:
    stream = llm.stream('Please write a long story about a programmer named Jack who created an AI assistant. The story should be at least 200 words.')
    
    chunk_count = 0
    for chunk in stream:
        if chunk.content:
            print(chunk.content, flush=True, end='')
            chunk_count += 1
    
    end_time = time.time()
    
    print()
    print()
    print('=' * 60)
    print(f'总共接收 {chunk_count} 个 chunk')
    print(f'耗时：{end_time - start_time:.2f}秒')
    print(f'平均每秒：{chunk_count / (end_time - start_time):.2f} 个 chunk')
except Exception as e:
    print(f"\n发生错误：{e}")
    import traceback
    traceback.print_exc()
