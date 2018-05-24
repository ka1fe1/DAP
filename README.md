---
layout: "post"
title: "readme.md"
date: "2017-10-30 17:00"
---

# Desc(项目描述)

Dap: data analyse process 用于数据分析和处理，主要用于处理 DCM 相关需求

---

# Init(初始化)

1. clone 下项目的地址后，使用 `pip` 命令安装项目依赖
> `pip install -r requirements_dev.txt`
>> **Note**：如果是在 Linux 系统中安装依赖，请使用 `requirements.txt`

2. 初始化环境配置：在 `conf/` 下根据自己的需求将 `env_xx.py.txt` 复制并重命名为 `env.py`，再根据自己的需求修改其内容。

3. 运行：
 - 非 Linux 环境：找到入口项目文件(`routes/index.py`)，直接运行即可
 - Linux 环境：使用 nginx + uwsgi 搭建运行环境

---

# Structure(项目结构)

该 project 是在轻量级框架 [`Flask`](http://flask.pocoo.org/) 的基础上进行开发的，其中作为服务(API)部分遵循 MVC 架构。

- `confs/`：配置文件
- `dto/`：data transport object 数据转换
- `modules/`：基础模块和工具类
- `routes/`：路由，入口文件在此目录中
- `services/`：业务逻辑层
- `vo/`：接收参数和返回响应
- `sql/`：存放 sql 文件目录
- `test/`：unit test

以下为额外目录的说明

- `dataAnalyse/`：数据分析和处理，并不提供 API 接口，一般用于一次性处理数据

---
