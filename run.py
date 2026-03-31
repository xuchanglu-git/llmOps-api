#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
启动脚本 - 用于直接运行应用
"""
import sys
import os

# 将项目根目录添加到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.http import app

if __name__ == "__main__":
    app.run(debug=True)
