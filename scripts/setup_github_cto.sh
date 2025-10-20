#!/bin/bash
# setup_github_cto.sh

# CTO GitHub全访问配置
# ⚠️ 请将下面的占位符替换为您的实际值
GITHUB_CTO_TOKEN="ghp_your_enhanced_token_here"
GITHUB_ORG="your-organization"

# 设置CTO访问权限
gh auth login --with-token <<< "$GITHUB_CTO_TOKEN"

# 配置仓库访问
echo "配置CTO对所有仓库的维护者权限..."
gh api -X PUT /orgs/$GITHUB_ORG/teams/cto-supervisors/memberships/cto-bot \
  -f role="maintainer"

# 设置自动化工作流
echo "部署CTO监督工作流..."
gh workflow enable cto-supervision.yml
gh workflow enable auto-code-review.yml

# 保护分支配置
echo "配置分支保护规则..."
for repo in $(gh repo list $GITHUB_ORG --json name -q '.[].name'); do
  echo "配置仓库: $repo"
  gh api -X PUT /repos/$GITHUB_ORG/$repo/branches/main/protection \
    -f required_status_checks='{"strict":true,"contexts":["cto-review"]}' \
    -f enforce_admins=true \
    -f required_pull_request_reviews='{"required_approving_review_count":1}' \
    -f restrictions=null || echo "跳过 $repo (可能不存在main分支)"
done

echo "✅ GitHub CTO配置完成"

