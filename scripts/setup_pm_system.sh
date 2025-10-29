#!/bin/bash
# AI PM 监督系统安装脚本

echo "🚀 正在安装AI PM监督系统..."

# 安装Python依赖
echo "📦 安装Python依赖..."
pip install -q pyyaml requests 2>/dev/null || pip3 install -q pyyaml requests

# 检查环境变量
echo "🔍 检查环境变量配置..."
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  警告: GITHUB_TOKEN未设置"
    echo "   请运行: export GITHUB_TOKEN=your_token_here"
fi

if [ -z "$VERCEL_TOKEN" ]; then
    echo "⚠️  警告: VERCEL_TOKEN未设置"
    echo "   请运行: export VERCEL_TOKEN=your_token_here"
fi

# 创建.env文件（如果不存在）
if [ ! -f .env ]; then
    echo "📝 创建.env配置文件..."
    cp .env.example .env
    echo "   请编辑.env文件并填入实际的凭证"
fi

echo "✅ AI PM监督系统安装完成!"
echo ""
echo "📚 使用指南:"
echo "   1. 编辑.env文件配置凭证"
echo "   2. 运行问题检测: python scripts/proactive_issue_detector.py ."
echo "   3. 查看FEATURE_UPDATE.md了解更多功能"
