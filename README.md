# llmops-api

基于 Flask 的 LLM 应用后端，集成 LangChain、LLM、Embedding 等能力。

## 目录结构

```
app/                  # 应用入口集合
config/               # 应用配置文件
internal/             # 应用内部文件夹
  core/               # LLM 核心（agent/chain/prompt/model_runtime/moderation/tool/vector_store）
  exception/          # 通用公共异常
  extension/          # Flask 扩展
  handler/            # 路由处理器 / 控制器
  middleware/         # 应用中间件
  migration/          # 数据库迁移文件
  model/              # 数据库模型
  router/             # 应用路由
  schedule/           # 调度 / 定时任务
  schema/             # 请求与响应结构体
  server/             # 构建的应用
  service/            # 服务层
  task/               # 任务（即时 + 延迟）
pkg/                  # 扩展包
  oauth/              # OAuth 实现
storage/              # 本地存储
test/                 # 测试目录
```

## 快速开始

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 复制环境变量
cp .env .env.local

# 运行
python app.py
```
