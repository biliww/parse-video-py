主要功能总结
触发条件：当有代码推送到 main-my 分支或针对该分支的拉取请求时自动触发
构建环境：使用 Ubuntu 最新版本作为构建环境
构建流程：检出代码 → 设置 Python 环境 → 登录 Docker Hub → 设置 Docker Buildx → 构建并推送镜像
输出结果：将构建的 Docker 镜像推送到 Docker Hub，标签为 latest，仅支持 linux/amd64 平台