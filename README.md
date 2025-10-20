# AI CTO 监督系统

一个定制化的AI CTO监督系统，用于自动化代码审查、项目监督和开发流程管理。

## 🎯 系统功能

### 核心功能

- **技术栈特定监督**：针对不同技术栈（React、Vue、Node.js、Python等）的专项监督规则
- **项目类型模板**：为Web应用、移动应用、API服务和桌面应用提供专门的监督模板
- **自动化代码审查**：通过GitHub Actions实现持续的代码质量检查
- **技术债务追踪**：自动检测和追踪未完成的功能、缺失的测试和安全问题
- **强制完成机制**：检测并干预不完整的开发工作

### 监督范围

✅ 功能完整性检查  
✅ 代码质量审计  
✅ 安全漏洞扫描  
✅ 测试覆盖率监控  
✅ 文档完整性验证  
✅ 部署配置审查  

## 📁 项目结构

```
aicto-system/
├── .github/
│   └── workflows/
│       └── cto-supervision-workflow.yml  # GitHub Actions工作流
├── scripts/
│   ├── project_supervisor.py            # 项目监督器
│   ├── manus_interaction_protocol.py    # Manus交互协议
│   ├── technical_debt_tracker.py        # 技术债务追踪器
│   └── setup_github_cto.sh              # GitHub配置脚本
├── cto-supervisor/
│   ├── Dockerfile                       # Docker镜像配置
│   ├── requirements.txt                 # Python依赖
│   └── supervisor_server.py             # 监督服务器
├── tech_stack_supervision.yaml          # 技术栈监督规则
├── database_supervision.sql             # 数据库监督配置
├── docker-compose.cto-supervision.yml   # Docker Compose配置
└── README.md                            # 本文档
```

## 🚀 快速开始

### 前置要求

- Docker 和 Docker Compose
- GitHub账户和Personal Access Token
- PostgreSQL（如果使用数据库监督功能）
- Python 3.11+（用于本地脚本）

### 安装步骤

#### 1. 克隆仓库

```bash
git clone https://github.com/EverestAn/aicto-system.git
cd aicto-system
```

#### 2. 配置环境变量

创建 `.env` 文件：

```bash
# GitHub配置
GITHUB_CTO_TOKEN=your_github_token_here
GITHUB_ORG=your-organization

# 数据库配置
DB_CTO_PASSWORD=your_secure_password_here
```

⚠️ **安全提示**：
- 不要将 `.env` 文件提交到Git仓库
- 使用强密码
- 定期轮换令牌

#### 3. 配置GitHub（可选）

如果需要自动化GitHub集成：

```bash
chmod +x scripts/setup_github_cto.sh
# 编辑脚本，填入您的实际值
nano scripts/setup_github_cto.sh
# 执行配置
./scripts/setup_github_cto.sh
```

#### 4. 初始化数据库（可选）

如果使用PostgreSQL监督功能：

```bash
psql -U postgres -f database_supervision.sql
```

#### 5. 启动监督服务

使用Docker Compose：

```bash
docker-compose -f docker-compose.cto-supervision.yml up -d
```

检查服务状态：

```bash
docker-compose -f docker-compose.cto-supervision.yml ps
```

## 📖 使用指南

### 技术栈监督

系统会根据 `tech_stack_supervision.yaml` 中定义的规则自动检查：

- **前端**：组件化、状态管理、路由、API集成
- **后端**：身份验证、数据验证、错误处理、日志记录
- **移动端**：导航、离线支持、推送通知

### 项目监督

使用项目监督器检查特定项目类型：

```bash
python3 scripts/project_supervisor.py
```

### 技术债务追踪

运行技术债务追踪器：

```bash
python3 scripts/technical_debt_tracker.py
```

这将生成 `technical_debt_report.json` 报告。

### Manus交互协议

使用交互协议发送开发指令：

```python
from scripts.manus_interaction_protocol import ManusInteractionProtocol

protocol = ManusInteractionProtocol()
requirements = {
    'complexity': 'medium',
    'features': ['用户认证', 'API集成'],
    'tests': ['单元测试', '集成测试']
}

directive = protocol.send_development_directive(
    "实现用户管理系统",
    requirements
)
print(directive)
```

## 🔧 配置说明

### GitHub Actions工作流

工作流会在以下情况触发：
- 推送到 `main` 或 `develop` 分支
- 创建针对 `main` 分支的Pull Request
- 每天早上9点和晚上6点（定时检查）

### Docker服务

系统包含三个主要服务：

1. **cto-supervisor**：主监督服务器
2. **code-auditor**：代码审计服务
3. **postgres-cto**：监督数据库

## 🛡️ 安全最佳实践

1. **令牌管理**：
   - 使用最小权限原则创建GitHub令牌
   - 设置令牌过期时间
   - 定期轮换令牌
   - 不要在代码中硬编码令牌

2. **密码安全**：
   - 使用强密码
   - 不要共享数据库凭证
   - 使用环境变量存储敏感信息

3. **访问控制**：
   - 限制CTO监督账户的权限范围
   - 定期审查访问日志
   - 启用双因素认证

## 📊 监督报告

系统会生成以下报告：

- **完整性审计报告**：检查功能完整性
- **技术债务报告**：追踪未完成的工作
- **安全审计报告**：识别安全漏洞
- **CTO干预报告**：记录需要人工干预的问题

## 🤝 与Manus的集成

系统专门设计用于监督Manus AI的开发工作，包括：

- 检测"偷懒模式"（只做界面不做逻辑、跳过测试等）
- 强制要求功能完整实现
- 自动化代码审查
- 实时进度追踪

## 🔍 故障排查

### 服务无法启动

```bash
# 检查日志
docker-compose -f docker-compose.cto-supervision.yml logs

# 检查端口占用
netstat -tuln | grep 8080
```

### GitHub Actions失败

- 检查仓库的Secrets配置
- 验证工作流文件语法
- 查看Actions日志

### 数据库连接问题

- 验证数据库凭证
- 检查网络连接
- 确认PostgreSQL服务运行中

## 📝 开发计划

- [ ] 实现完整的代码审计引擎
- [ ] 添加更多技术栈支持
- [ ] 集成AI代码分析
- [ ] 开发Web管理界面
- [ ] 支持多语言项目

## 📄 许可证

MIT License

## 👥 贡献

欢迎提交Issue和Pull Request！

## 📧 联系方式

如有问题，请通过GitHub Issues联系。

---

**⚠️ 重要提示**：本系统设计用于开发环境监督。在生产环境使用前，请确保进行充分的安全审查和测试。

