#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/3/29 14:59
@Author  : thezehui@gmail.com
@File    : app_handler.py
"""
import os
import uuid
from uuid  import UUID
from dataclasses import dataclass

from injector import inject
from flask import request
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openai import OpenAI

from internal.exception import FailException
from internal.schema.app_schema import CompletionReq
from internal.service import AppService
from pkg.response import success_json, validate_error_json, success_message


@inject
@dataclass
class AppHandler:
    """应用控制器"""
    app_service: AppService

    def create_app(self):
        """调用服务创建新的APP记录"""
        app = self.app_service.create_app()
        return success_message(f"应用已经成功创建，id为{app.id}")

    def get_app(self, id: UUID):
        app = self.app_service.get_app(id)
        return success_message(f"应用已经成功获取，名字是{app.name}")

    def update_app(self, id: UUID):
        app = self.app_service.update_app(id)
        return success_message(f"应用已经成功修改，修改的名字是:{app.name}")

    def delete_app(self, id: UUID):
        app = self.app_service.delete_app(id)
        return success_message(f"应用已经成功删除，id 为:{app.id}")

    def debug(self, id: UUID):
        """聊天接口"""
        # 打印所有参数
        print(f"\n{'='*60}")
        print(f"URL 参数 - id: {id}")
        print(f"Request 方法：{request.method}")
        print(f"Request Headers: {dict(request.headers)}")
        print(f"Request JSON Body: {request.get_json()}")
        print(f"{'='*60}\n")
        
        # 1.提取从接口中获取的输入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.构建组件
        prompt = ChatPromptTemplate.from_template("{query}")
        # llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
        llm = ChatOpenAI(
            api_key="sk-r1dmsG2q5wO2WmXYeNxoaJBkDiiS2Tm3UHQBtprC4JSdUWXT",
            base_url="https://api.moonshot.cn/v1",
            model="kimi-k2.5",
        )

        parser = StrOutputParser()

        # 3.构建链
        chain = prompt | llm | parser

        # 4.调用链得到结果
        content = chain.invoke({"query": req.query.data})

        return success_json({"content": content})

    def completion(self):
        """聊天接口"""
        # 1.提取从接口中获取的输入，POST
        req = CompletionReq()
        if not req.validate():
            return validate_error_json(req.errors)

        # 2.构建OpenAI客户端，并发起请求
        # client = OpenAI(base_url=os.getenv("OPENAI_API_BASE"))
        client = OpenAI(
            api_key="sk-r1dmsG2q5wO2WmXYeNxoaJBkDiiS2Tm3UHQBtprC4JSdUWXT",
            base_url="https://api.moonshot.cn/v1",
        )


        # 3.得到请求响应，然后将OpenAI的响应传递给前端
        completion = client.chat.completions.create(
            # model="gpt-3.5-turbo-16k",
            model="kimi-k2.5",
            messages = [
                {"role": "system", "content": "你是OpenAI开发的聊天机器人，请根据用户的输入回复对应的信息"},
                {"role": "user", "content": req.query.data},
            ],
            stream=True,
        )

        content = completion.choices[0].message.content

        return success_json({"content": content})

    def ping(self):
        # raise FailException("数据未找到")
        return success_json({"ping": "pong"})
