#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/6/8 22:11
@Author  : thezehui@gmail.com
@File    : 4.复用提示模板.py
"""
from langchain_core.prompts import PromptTemplate

# 描述模板
instruction_prompt = PromptTemplate.from_template("你正在模拟{person}")

# 示例模板
example_prompt = PromptTemplate.from_template("""下面是一个交互例子：

Q: {example_q}
A: {example_a}""")

# 开始模板
start_prompt = PromptTemplate.from_template("""现在，你是一个真实的人，请回答用户的问题:

Q: {input}
A:""")

# 手动组合多个模板（替代 PipelinePromptTemplate）
def create_pipeline_prompt(person, example_q, example_a, input):
    instruction = instruction_prompt.format(person=person)
    example = example_prompt.format(example_q=example_q, example_a=example_a)
    start = start_prompt.format(input=input)
    
    return f"{instruction}\n\n{example}\n\n{start}"

print(create_pipeline_prompt(
    person="雷军",
    example_q="你最喜欢的汽车是什么？",
    example_a="小米 su7",
    input="你最喜欢的手机是什么？"
))
