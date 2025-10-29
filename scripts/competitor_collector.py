#!/usr/bin/env python3
"""
竞品信息采集模块
自动采集竞品的功能特性、技术栈、用户反馈等信息
"""

import os
import json
import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


@dataclass
class Competitor:
    """竞品数据模型"""
    id: str
    name: str
    category: str  # direct, indirect, potential
    website: str
    github_repo: Optional[str] = None
    description: str = ""
    features: List[Dict[str, Any]] = None
    tech_stack: List[str] = None
    pricing: Dict[str, Any] = None
    user_reviews: List[Dict[str, Any]] = None
    discovered_at: str = None
    last_updated: str = None
    
    def __post_init__(self):
        if self.features is None:
            self.features = []
        if self.tech_stack is None:
            self.tech_stack = []
        if self.pricing is None:
            self.pricing = {}
        if self.user_reviews is None:
            self.user_reviews = []
        if self.discovered_at is None:
            self.discovered_at = datetime.now().isoformat()
        if self.last_updated is None:
            self.last_updated = datetime.now().isoformat()


class CompetitorCollector:
    """竞品信息采集器"""
    
    def __init__(self, data_dir: str = "./data/competitors"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.github_token = os.environ.get('GITHUB_TOKEN', '')
        
    def discover_competitors(self, product_description: str, keywords: List[str]) -> List[str]:
        """
        自动发现竞品
        
        Args:
            product_description: 产品描述
            keywords: 关键词列表
            
        Returns:
            竞品名称列表
        """
        print(f"🔍 根据产品描述和关键词发现竞品...")
        print(f"   产品描述: {product_description[:100]}...")
        print(f"   关键词: {', '.join(keywords)}")
        
        # 这里可以集成搜索API或使用LLM来发现竞品
        # 目前返回预定义的竞品列表作为示例
        
        competitors = []
        
        # 示例：AI代码审查工具竞品
        if any(kw in product_description.lower() for kw in ['code review', 'ai', 'pm', 'supervisor']):
            competitors.extend([
                'CodeRabbit',
                'Qodo Merge',
                'GitHub Copilot',
                'SonarQube',
                'Codacy',
                'DeepCode',
                'Snyk Code'
            ])
        
        print(f"   发现 {len(competitors)} 个潜在竞品")
        return competitors
    
    def collect_github_info(self, repo_url: str) -> Dict[str, Any]:
        """
        采集GitHub仓库信息
        
        Args:
            repo_url: GitHub仓库URL
            
        Returns:
            仓库信息字典
        """
        print(f"   📦 采集GitHub信息: {repo_url}")
        
        # 解析仓库所有者和名称
        parts = repo_url.replace('https://github.com/', '').replace('.git', '').split('/')
        if len(parts) < 2:
            return {}
        
        owner, repo = parts[0], parts[1]
        
        try:
            headers = {}
            if self.github_token:
                headers['Authorization'] = f'token {self.github_token}'
            
            # 获取仓库基本信息
            api_url = f'https://api.github.com/repos/{owner}/{repo}'
            response = requests.get(api_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                repo_data = response.json()
                
                info = {
                    'stars': repo_data.get('stargazers_count', 0),
                    'forks': repo_data.get('forks_count', 0),
                    'watchers': repo_data.get('watchers_count', 0),
                    'open_issues': repo_data.get('open_issues_count', 0),
                    'description': repo_data.get('description', ''),
                    'language': repo_data.get('language', ''),
                    'topics': repo_data.get('topics', []),
                    'created_at': repo_data.get('created_at', ''),
                    'updated_at': repo_data.get('updated_at', ''),
                    'homepage': repo_data.get('homepage', ''),
                }
                
                # 获取README
                readme_url = f'https://api.github.com/repos/{owner}/{repo}/readme'
                readme_response = requests.get(readme_url, headers=headers, timeout=10)
                if readme_response.status_code == 200:
                    readme_data = readme_response.json()
                    info['readme_url'] = readme_data.get('html_url', '')
                
                print(f"      ✓ Stars: {info['stars']}, Language: {info['language']}")
                return info
            else:
                print(f"      ✗ GitHub API返回 {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"      ✗ 采集GitHub信息失败: {e}")
            return {}
    
    def collect_competitor_info(self, name: str, website: str = None, github_repo: str = None) -> Competitor:
        """
        采集单个竞品的完整信息
        
        Args:
            name: 竞品名称
            website: 官网URL
            github_repo: GitHub仓库URL
            
        Returns:
            Competitor对象
        """
        print(f"\n📊 采集竞品信息: {name}")
        
        competitor = Competitor(
            id=name.lower().replace(' ', '-'),
            name=name,
            category='direct',  # 默认为直接竞品
            website=website or f"https://{name.lower().replace(' ', '')}.com",
            github_repo=github_repo
        )
        
        # 采集GitHub信息
        if github_repo:
            github_info = self.collect_github_info(github_repo)
            if github_info:
                competitor.description = github_info.get('description', '')
                competitor.tech_stack = [github_info.get('language', '')] + github_info.get('topics', [])
                competitor.tech_stack = [t for t in competitor.tech_stack if t]  # 移除空值
        
        # 这里可以添加更多采集逻辑：
        # - 爬取官网获取功能列表
        # - 采集用户评论
        # - 分析定价策略
        # 目前使用占位符数据
        
        competitor.features = [
            {
                'name': 'AI代码审查',
                'description': '使用AI自动审查代码质量',
                'category': 'core'
            }
        ]
        
        return competitor
    
    def save_competitor(self, competitor: Competitor):
        """保存竞品信息到文件"""
        file_path = self.data_dir / f"{competitor.id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(competitor), f, indent=2, ensure_ascii=False)
        print(f"   💾 已保存到: {file_path}")
    
    def load_competitor(self, competitor_id: str) -> Optional[Competitor]:
        """从文件加载竞品信息"""
        file_path = self.data_dir / f"{competitor_id}.json"
        if not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return Competitor(**data)
    
    def list_competitors(self) -> List[str]:
        """列出所有已采集的竞品"""
        return [f.stem for f in self.data_dir.glob('*.json')]
    
    def collect_batch(self, competitors_config: List[Dict[str, str]]) -> List[Competitor]:
        """
        批量采集竞品信息
        
        Args:
            competitors_config: 竞品配置列表，每项包含name, website, github_repo
            
        Returns:
            Competitor对象列表
        """
        print(f"\n🚀 开始批量采集 {len(competitors_config)} 个竞品的信息...\n")
        
        competitors = []
        for config in competitors_config:
            try:
                competitor = self.collect_competitor_info(
                    name=config['name'],
                    website=config.get('website'),
                    github_repo=config.get('github_repo')
                )
                self.save_competitor(competitor)
                competitors.append(competitor)
            except Exception as e:
                print(f"   ✗ 采集 {config['name']} 失败: {e}")
        
        print(f"\n✅ 批量采集完成，成功采集 {len(competitors)} 个竞品")
        return competitors
    
    def generate_summary(self) -> Dict[str, Any]:
        """生成竞品数据摘要"""
        competitor_ids = self.list_competitors()
        
        summary = {
            'total_competitors': len(competitor_ids),
            'competitors': [],
            'generated_at': datetime.now().isoformat()
        }
        
        for comp_id in competitor_ids:
            competitor = self.load_competitor(comp_id)
            if competitor:
                summary['competitors'].append({
                    'id': competitor.id,
                    'name': competitor.name,
                    'category': competitor.category,
                    'website': competitor.website,
                    'features_count': len(competitor.features),
                    'tech_stack': competitor.tech_stack,
                    'last_updated': competitor.last_updated
                })
        
        return summary


def main():
    """主函数 - 示例用法"""
    collector = CompetitorCollector()
    
    # 示例：采集AI代码审查工具竞品
    competitors_config = [
        {
            'name': 'CodeRabbit',
            'website': 'https://coderabbit.ai',
            'github_repo': None  # CodeRabbit是商业产品，没有公开仓库
        },
        {
            'name': 'Qodo Merge',
            'website': 'https://www.qodo.ai',
            'github_repo': None
        },
        {
            'name': 'SonarQube',
            'website': 'https://www.sonarsource.com/products/sonarqube',
            'github_repo': 'https://github.com/SonarSource/sonarqube'
        }
    ]
    
    # 批量采集
    competitors = collector.collect_batch(competitors_config)
    
    # 生成摘要
    summary = collector.generate_summary()
    
    # 保存摘要
    summary_path = collector.data_dir / 'summary.json'
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 摘要已保存到: {summary_path}")
    print(f"\n📊 竞品数据统计:")
    print(f"   总计: {summary['total_competitors']} 个竞品")
    for comp in summary['competitors']:
        print(f"   - {comp['name']}: {comp['features_count']} 个功能")


if __name__ == '__main__':
    main()
