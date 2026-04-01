#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/6/9 19:03
@Author  : thezehui@gmail.com
@File    : 3.Model流式输出.py
"""
import time
from datetime import datetime

import dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

dotenv.load_dotenv()

# 1.编排 prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是 OpenAI 开发的聊天机器人，请回答用户的问题，现在的时间是{now}"),
    ("human", "{query}"),
]).partial(now=datetime.now())

# 2.创建大语言模型
# 注意：不需要设置 streaming=True，.stream() 方法本身就支持流式输出
llm = ChatOpenAI(
    api_key="sk-r1dmsG2q5wO2WmXYeNxoaJBkDiiS2Tm3UHQBtprC4JSdUWXT",
    base_url="https://api.moonshot.cn/v1",
    model="kimi-k2.5",
)

# 3.流式输出
print("开始流式输出测试：\n")
print("=" * 60)
print()

start_time = time.time()
chunk_count = 0
first_chunk_time = None

try:
    response = llm.stream(prompt.invoke({"query": "你能简单介绍下 LLM 和 LLMOps 吗？请用至少 200 字详细回答。"}))
    
    for chunk in response:
        # 记录第一个 chunk 的时间
        if first_chunk_time is None:
            first_chunk_time = time.time()
            print(f"[首字耗时：{first_chunk_time - start_time:.2f}秒]\n")
        
        # chunk.content 可能为 None 或空字符串，需要判断
        if chunk.content:
            print(chunk.content, flush=True, end='')
            chunk_count += 1
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print()
    print()
    print("=" * 60)
    print(f"✅ 流式输出完成")
    print(f"📊 统计数据：")
    print(f"   - 总耗时：{total_time:.2f}秒")
    print(f"   - 接收 chunk 数：{chunk_count}")
    print(f"   - 平均每秒：{chunk_count / total_time:.2f} 个 chunk")
    print(f"   - 首字延迟：{first_chunk_time - start_time:.2f}秒")
    
except Exception as e:
    print(f"\n❌ 发生错误：{e}")
    import traceback
    traceback.print_exc()
