# AI PM 智能竞品分析系统 - 使用指南

## 概述

智能竞品分析系统是AI PM监督系统的核心智能模块，能够自动分析市面上的竞品，提取功能特性，对比差异，并生成具体的功能迭代建议和实施步骤。

## 核心功能

### 1. 竞品信息采集
- 自动采集GitHub仓库信息（Stars、语言、主题等）
- 支持批量采集多个竞品
- 数据持久化存储

### 2. 智能分析
- 使用LLM提取竞品功能特性
- 对比功能差距
- 识别优势和劣势

### 3. 建议生成
- 自动生成功能迭代建议
- 优先级排序
- 详细的实施步骤和风险评估

## 快速开始

### 安装依赖

```bash
# 安装Python依赖
pip install requests openai

# 配置环境变量
export GITHUB_TOKEN="your_github_token"
export OPENAI_API_KEY="your_openai_api_key"
```

### 基本用法

#### 1. 列出已采集的竞品

```bash
python scripts/ai_pm_cli.py list
```

#### 2. 采集竞品信息

**单个采集**:
```bash
python scripts/ai_pm_cli.py collect \
  --name "CodeRabbit" \
  --website "https://coderabbit.ai"
```

**批量采集**:
```bash
# 创建配置文件 competitors.json
cat > competitors.json << 'EOF'
[
  {
    "name": "CodeRabbit",
    "website": "https://coderabbit.ai"
  },
  {
    "name": "SonarQube",
    "website": "https://www.sonarsource.com/products/sonarqube",
    "github_repo": "https://github.com/SonarSource/sonarqube"
  }
]
EOF

# 执行批量采集
python scripts/ai_pm_cli.py collect --config competitors.json
```

#### 3. 分析竞品并生成报告

```bash
# 执行分析（同时生成JSON和Markdown报告）
python scripts/ai_pm_cli.py analyze --markdown

# 自定义产品描述
python scripts/ai_pm_cli.py analyze \
  --our-description "我的AI产品描述" \
  --markdown
```

#### 4. 查看分析报告

```bash
# 查看报告摘要
python scripts/ai_pm_cli.py report

# 查看更多建议
python scripts/ai_pm_cli.py report --suggestions 10
```

## 目录结构

```
aicto-system/
├── scripts/
│   ├── ai_pm_cli.py              # CLI主程序
│   ├── competitor_collector.py   # 竞品信息采集模块
│   └── competitor_analyzer.py    # 智能分析模块
├── data/
│   ├── competitors/              # 竞品数据存储
│   │   ├── coderabbit.json
│   │   ├── sonarqube.json
│   │   └── ...
│   └── analysis/                 # 分析报告存储
│       ├── analysis_report.json
│       └── analysis_report.md
└── docs/
    ├── competitor_analysis_system_design.md  # 系统设计文档
    └── COMPETITOR_ANALYSIS_README.md         # 使用指南
```

## 数据模型

### 竞品数据 (Competitor)

```json
{
  "id": "coderabbit",
  "name": "CodeRabbit",
  "category": "direct",
  "website": "https://coderabbit.ai",
  "github_repo": null,
  "description": "AI代码审查工具",
  "features": [
    {
      "name": "AI代码审查",
      "description": "使用AI自动审查代码质量",
      "category": "core"
    }
  ],
  "tech_stack": ["Python", "AI"],
  "pricing": {},
  "user_reviews": [],
  "discovered_at": "2025-10-29T14:00:00",
  "last_updated": "2025-10-29T14:00:00"
}
```

### 分析报告 (Analysis Report)

```json
{
  "analysis_date": "2025-10-29T14:48:51",
  "our_product": {
    "description": "AI PM监督系统",
    "features_count": 4
  },
  "competitors_analyzed": 3,
  "total_gaps": 3,
  "total_suggestions": 3,
  "high_priority_suggestions": 3,
  "suggestions": [
    {
      "id": "sugg-20251029-001",
      "title": "实现AI代码审查功能",
      "description": "参考CodeRabbit实现...",
      "source_competitor": "CodeRabbit",
      "priority": 4,
      "impact": "high",
      "effort": "medium",
      "implementation_steps": [...],
      "estimated_time": "2-4周",
      "required_resources": ["开发工程师1名"],
      "risks": [...],
      "user_benefit": "...",
      "business_value": "...",
      "competitive_advantage": "..."
    }
  ]
}
```

## 高级用法

### 1. 自定义数据目录

```bash
python scripts/ai_pm_cli.py analyze \
  --data-dir ./custom/competitors \
  --output-dir ./custom/analysis
```

### 2. 发现竞品（实验性功能）

```bash
python scripts/ai_pm_cli.py discover \
  --description "AI代码审查工具" \
  --keywords "ai,code review,automation"
```

### 3. 编程方式使用

```python
from scripts.competitor_collector import CompetitorCollector
from scripts.competitor_analyzer import CompetitorAnalyzer

# 采集竞品
collector = CompetitorCollector()
competitor = collector.collect_competitor_info(
    name="CodeRabbit",
    website="https://coderabbit.ai"
)
collector.save_competitor(competitor)

# 分析竞品
analyzer = CompetitorAnalyzer()
our_features = [
    {"name": "代码质量检查", "description": "...", "category": "core"}
]
report = analyzer.analyze_all_competitors(
    our_product_description="AI PM监督系统",
    our_features=our_features
)

# 保存报告
analyzer.save_report(report)
```

## 配置说明

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| `GITHUB_TOKEN` | GitHub API Token | 推荐 |
| `OPENAI_API_KEY` | OpenAI API Key | 必需（用于LLM分析） |

### GitHub Token权限

需要以下权限：
- `repo` (读取公开仓库)
- `read:org` (读取组织信息，可选)

### OpenAI API配置

支持的模型：
- `gpt-4.1-mini` (默认，平衡性能和成本)
- `gpt-4.1-nano` (快速响应)
- `gemini-2.5-flash` (Google模型)

## 输出报告

### JSON报告

位置: `data/analysis/analysis_report.json`

包含完整的分析数据，适合程序化处理。

### Markdown报告

位置: `data/analysis/analysis_report.md`

包含：
- 执行摘要
- 竞品概览
- 功能对比矩阵
- 差距分析
- 迭代建议（按优先级排序）
- 趋势洞察

## 工作流程

```
1. 定义产品和功能
   ↓
2. 采集竞品信息
   ├─ 手动指定竞品
   └─ 自动发现竞品（实验性）
   ↓
3. 执行智能分析
   ├─ 提取竞品功能（LLM）
   ├─ 对比功能差距
   └─ 识别优势劣势
   ↓
4. 生成迭代建议
   ├─ 功能建议
   ├─ 优先级排序
   ├─ 实施路径
   └─ 风险评估
   ↓
5. 输出报告
   ├─ JSON格式
   └─ Markdown格式
   ↓
6. 审查和执行
```

## 最佳实践

### 1. 定期更新竞品数据

建议每周或每月重新采集竞品信息，追踪变化趋势。

```bash
# 创建定时任务
crontab -e

# 每周一上午9点执行
0 9 * * 1 cd /path/to/aicto-system && python scripts/ai_pm_cli.py collect --config competitors.json
```

### 2. 结合人工审查

LLM生成的建议应该由产品经理和技术负责人审查，结合实际情况调整优先级。

### 3. 追踪实施进度

将建议导入项目管理工具（如GitHub Issues、Jira），追踪实施进度。

```bash
# 可以基于报告自动创建GitHub Issues
# （需要实现）
```

### 4. 持续优化

根据实施反馈，优化分析策略和建议生成逻辑。

## 故障排查

### 问题1: LLM不可用

**症状**: 显示"LLM不可用"警告

**解决方案**:
1. 检查是否安装了openai库: `pip install openai`
2. 检查环境变量: `echo $OPENAI_API_KEY`
3. 验证API Key有效性

### 问题2: GitHub API限流

**症状**: GitHub API返回403错误

**解决方案**:
1. 配置GITHUB_TOKEN环境变量
2. 检查Token权限
3. 等待限流重置（通常1小时）

### 问题3: 采集数据不完整

**症状**: 竞品功能列表为空

**解决方案**:
1. 检查竞品是否有公开的GitHub仓库
2. 手动补充功能信息到JSON文件
3. 使用LLM从产品描述中提取功能

## 扩展开发

### 添加新的数据源

编辑 `competitor_collector.py`，添加新的采集方法：

```python
def collect_product_hunt_info(self, product_name: str) -> Dict[str, Any]:
    """采集Product Hunt信息"""
    # 实现逻辑
    pass
```

### 自定义分析逻辑

编辑 `competitor_analyzer.py`，添加自定义分析：

```python
def analyze_user_sentiment(self, reviews: List[Dict]) -> str:
    """分析用户情感"""
    # 实现逻辑
    pass
```

### 集成到CI/CD

在GitHub Actions中自动执行竞品分析：

```yaml
name: Competitor Analysis

on:
  schedule:
    - cron: '0 9 * * 1'  # 每周一上午9点

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Analysis
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          pip install requests openai
          python scripts/ai_pm_cli.py analyze --markdown
      - name: Upload Report
        uses: actions/upload-artifact@v4
        with:
          name: analysis-report
          path: data/analysis/
```

## 贡献指南

欢迎贡献代码和建议！

1. Fork项目
2. 创建功能分支
3. 提交Pull Request

## 许可证

[待定]

## 联系方式

- 项目仓库: https://github.com/everest-an/aicto-system
- Issues: https://github.com/everest-an/aicto-system/issues

---

**版本**: 1.0  
**更新时间**: 2025-10-30  
**作者**: AI PM Team
