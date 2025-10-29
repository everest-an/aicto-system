#!/usr/bin/env python3
"""
智能竞品分析和建议生成模块
使用LLM分析竞品特性，生成功能迭代建议
"""

import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import sys

# 尝试导入OpenAI客户端
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("⚠️  OpenAI库未安装，请运行: pip install openai")


@dataclass
class FeatureGap:
    """功能差距"""
    feature_name: str
    description: str
    exists_in_our_product: bool
    competitor_implementation: str
    gap_severity: str  # critical, high, medium, low
    user_impact: str


@dataclass
class IterationSuggestion:
    """迭代建议"""
    id: str
    title: str
    description: str
    source_competitor: str
    source_feature: str
    priority: int  # 1-5, 5最高
    impact: str  # high, medium, low
    effort: str  # high, medium, low
    implementation_steps: List[str]
    estimated_time: str
    required_resources: List[str]
    risks: List[str]
    user_benefit: str
    business_value: str
    competitive_advantage: str
    status: str = "pending"
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


class CompetitorAnalyzer:
    """竞品分析器"""
    
    def __init__(self, data_dir: str = "./data/competitors", output_dir: str = "./data/analysis"):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化LLM客户端
        self.llm_available = False
        if OPENAI_AVAILABLE and os.environ.get('OPENAI_API_KEY'):
            try:
                self.client = OpenAI()  # API key从环境变量自动读取
                self.llm_available = True
                print("✅ LLM客户端初始化成功")
            except Exception as e:
                print(f"⚠️  LLM客户端初始化失败: {e}")
        else:
            print("⚠️  LLM不可用（缺少OpenAI API Key或库未安装）")
    
    def load_competitor_data(self, competitor_id: str) -> Optional[Dict[str, Any]]:
        """加载竞品数据"""
        file_path = self.data_dir / f"{competitor_id}.json"
        if not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_all_competitors(self) -> List[Dict[str, Any]]:
        """加载所有竞品数据"""
        competitors = []
        for file_path in self.data_dir.glob('*.json'):
            if file_path.name == 'summary.json':
                continue
            with open(file_path, 'r', encoding='utf-8') as f:
                competitors.append(json.load(f))
        return competitors
    
    def analyze_with_llm(self, prompt: str, model: str = "gpt-4.1-mini") -> str:
        """
        使用LLM进行分析
        
        Args:
            prompt: 分析提示
            model: 模型名称
            
        Returns:
            LLM响应文本
        """
        if not self.llm_available:
            return "LLM不可用，无法执行智能分析"
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的产品经理和技术分析师，擅长分析竞品功能并提供产品迭代建议。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"⚠️  LLM分析失败: {e}")
            return f"分析失败: {e}"
    
    def extract_features_from_competitor(self, competitor: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        从竞品数据中提取功能特性
        
        Args:
            competitor: 竞品数据
            
        Returns:
            功能列表
        """
        print(f"   🔍 提取 {competitor['name']} 的功能特性...")
        
        # 如果已有功能列表，直接返回
        if competitor.get('features'):
            return competitor['features']
        
        # 否则使用LLM从描述中提取
        if self.llm_available and competitor.get('description'):
            prompt = f"""
分析以下产品描述，提取其核心功能特性：

产品名称: {competitor['name']}
产品描述: {competitor['description']}
技术栈: {', '.join(competitor.get('tech_stack', []))}

请以JSON数组格式返回功能列表，每个功能包含：
- name: 功能名称
- description: 功能描述
- category: 功能分类（core/advanced/integration）

示例格式：
[
  {{"name": "AI代码审查", "description": "使用AI自动审查代码质量", "category": "core"}},
  {{"name": "自动修复建议", "description": "提供代码修复建议", "category": "advanced"}}
]
"""
            response = self.analyze_with_llm(prompt)
            try:
                # 尝试解析JSON
                import re
                json_match = re.search(r'\[.*\]', response, re.DOTALL)
                if json_match:
                    features = json.loads(json_match.group())
                    print(f"      ✓ 提取到 {len(features)} 个功能")
                    return features
            except:
                pass
        
        # 默认返回空列表
        return []
    
    def compare_features(self, our_features: List[Dict[str, str]], 
                        competitor_features: List[Dict[str, str]],
                        competitor_name: str) -> List[FeatureGap]:
        """
        对比功能差距
        
        Args:
            our_features: 我们的功能列表
            competitor_features: 竞品功能列表
            competitor_name: 竞品名称
            
        Returns:
            功能差距列表
        """
        print(f"   📊 对比与 {competitor_name} 的功能差距...")
        
        gaps = []
        our_feature_names = {f['name'].lower() for f in our_features}
        
        for comp_feature in competitor_features:
            feature_name = comp_feature['name']
            exists = feature_name.lower() in our_feature_names
            
            # 简单的严重程度判断（实际应该用LLM分析）
            if not exists:
                severity = 'high' if comp_feature.get('category') == 'core' else 'medium'
            else:
                severity = 'low'
            
            gap = FeatureGap(
                feature_name=feature_name,
                description=comp_feature.get('description', ''),
                exists_in_our_product=exists,
                competitor_implementation=f"{competitor_name}的实现",
                gap_severity=severity,
                user_impact='需要分析'
            )
            gaps.append(gap)
        
        print(f"      ✓ 发现 {len([g for g in gaps if not g.exists_in_our_product])} 个缺失功能")
        return gaps
    
    def generate_suggestions(self, gaps: List[FeatureGap], 
                           competitor_name: str,
                           our_product_context: str = "") -> List[IterationSuggestion]:
        """
        基于功能差距生成迭代建议
        
        Args:
            gaps: 功能差距列表
            competitor_name: 竞品名称
            our_product_context: 我们产品的上下文信息
            
        Returns:
            迭代建议列表
        """
        print(f"   💡 生成迭代建议...")
        
        suggestions = []
        
        # 只为缺失的功能生成建议
        missing_gaps = [g for g in gaps if not g.exists_in_our_product and g.gap_severity in ['critical', 'high']]
        
        for i, gap in enumerate(missing_gaps[:10]):  # 限制最多10个建议
            # 计算优先级（5最高，1最低）
            priority = 5 if gap.gap_severity == 'critical' else 4 if gap.gap_severity == 'high' else 3
            
            suggestion = IterationSuggestion(
                id=f"sugg-{datetime.now().strftime('%Y%m%d')}-{i+1:03d}",
                title=f"实现{gap.feature_name}功能",
                description=f"参考{competitor_name}，实现{gap.feature_name}功能。{gap.description}",
                source_competitor=competitor_name,
                source_feature=gap.feature_name,
                priority=priority,
                impact='high' if gap.gap_severity in ['critical', 'high'] else 'medium',
                effort='medium',  # 默认中等难度
                implementation_steps=[
                    f"1. 研究{competitor_name}的{gap.feature_name}实现方式",
                    "2. 设计我们的实现方案",
                    "3. 开发核心功能",
                    "4. 编写测试用例",
                    "5. 文档编写和用户指南"
                ],
                estimated_time="2-4周",
                required_resources=["开发工程师1名", "测试工程师1名"],
                risks=[
                    "技术实现复杂度可能超出预期",
                    "需要额外的第三方服务支持"
                ],
                user_benefit=f"用户可以使用{gap.feature_name}功能，提升产品体验",
                business_value="增强产品竞争力，吸引更多用户",
                competitive_advantage=f"缩小与{competitor_name}的功能差距"
            )
            suggestions.append(suggestion)
        
        print(f"      ✓ 生成 {len(suggestions)} 条建议")
        return suggestions
    
    def analyze_all_competitors(self, our_product_description: str,
                                our_features: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        分析所有竞品并生成综合报告
        
        Args:
            our_product_description: 我们产品的描述
            our_features: 我们的功能列表
            
        Returns:
            分析报告
        """
        print(f"\n🚀 开始分析所有竞品...\n")
        
        competitors = self.load_all_competitors()
        print(f"📊 加载了 {len(competitors)} 个竞品数据\n")
        
        all_gaps = []
        all_suggestions = []
        competitor_summaries = []
        
        for competitor in competitors:
            print(f"📌 分析竞品: {competitor['name']}")
            
            # 提取竞品功能
            comp_features = self.extract_features_from_competitor(competitor)
            
            # 对比功能差距
            gaps = self.compare_features(our_features, comp_features, competitor['name'])
            all_gaps.extend(gaps)
            
            # 生成迭代建议
            suggestions = self.generate_suggestions(gaps, competitor['name'], our_product_description)
            all_suggestions.extend(suggestions)
            
            # 竞品摘要
            summary = {
                'name': competitor['name'],
                'website': competitor['website'],
                'features_count': len(comp_features),
                'gaps_count': len([g for g in gaps if not g.exists_in_our_product]),
                'suggestions_count': len(suggestions)
            }
            competitor_summaries.append(summary)
            print()
        
        # 按优先级排序建议
        all_suggestions.sort(key=lambda x: x.priority, reverse=True)
        
        # 生成报告
        report = {
            'analysis_date': datetime.now().isoformat(),
            'our_product': {
                'description': our_product_description,
                'features_count': len(our_features)
            },
            'competitors_analyzed': len(competitors),
            'competitor_summaries': competitor_summaries,
            'total_gaps': len([g for g in all_gaps if not g.exists_in_our_product]),
            'total_suggestions': len(all_suggestions),
            'high_priority_suggestions': len([s for s in all_suggestions if s.priority >= 4]),
            'suggestions': [asdict(s) for s in all_suggestions[:20]]  # 只保留前20个
        }
        
        print(f"✅ 分析完成!")
        print(f"   - 分析竞品: {len(competitors)} 个")
        print(f"   - 发现差距: {report['total_gaps']} 个")
        print(f"   - 生成建议: {report['total_suggestions']} 条")
        print(f"   - 高优先级: {report['high_priority_suggestions']} 条")
        
        return report
    
    def save_report(self, report: Dict[str, Any], filename: str = "analysis_report.json"):
        """保存分析报告"""
        file_path = self.output_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n💾 报告已保存到: {file_path}")
        return file_path
    
    def generate_markdown_report(self, report: Dict[str, Any]) -> str:
        """生成Markdown格式的分析报告"""
        md = f"""# 竞品分析报告

**分析时间**: {report['analysis_date']}

## 执行摘要

本次分析了 **{report['competitors_analyzed']}** 个竞品，发现 **{report['total_gaps']}** 个功能差距，生成 **{report['total_suggestions']}** 条迭代建议，其中 **{report['high_priority_suggestions']}** 条为高优先级建议。

## 我们的产品

**描述**: {report['our_product']['description']}

**现有功能数**: {report['our_product']['features_count']} 个

## 竞品概览

"""
        for comp in report['competitor_summaries']:
            md += f"""### {comp['name']}

- **官网**: {comp['website']}
- **功能数**: {comp['features_count']} 个
- **功能差距**: {comp['gaps_count']} 个
- **生成建议**: {comp['suggestions_count']} 条

"""
        
        md += """## 迭代建议

### 高优先级建议

"""
        high_priority = [s for s in report['suggestions'] if s['priority'] >= 4]
        for i, sugg in enumerate(high_priority[:10], 1):
            md += f"""#### {i}. {sugg['title']}

**来源**: {sugg['source_competitor']} - {sugg['source_feature']}  
**优先级**: {sugg['priority']}/5 | **影响**: {sugg['impact']} | **难度**: {sugg['effort']}

**描述**: {sugg['description']}

**用户收益**: {sugg['user_benefit']}

**实施步骤**:
"""
            for step in sugg['implementation_steps']:
                md += f"{step}\n"
            
            md += f"""
**预估时间**: {sugg['estimated_time']}

**所需资源**: {', '.join(sugg['required_resources'])}

**风险点**: {', '.join(sugg['risks'])}

---

"""
        
        md += """## 总结

通过本次竞品分析，我们识别了关键的功能差距和改进机会。建议优先实施高优先级建议，以快速缩小与竞品的差距，提升产品竞争力。

"""
        return md


def main():
    """主函数 - 示例用法"""
    analyzer = CompetitorAnalyzer()
    
    # 定义我们的产品
    our_product_description = "AI PM监督系统 - 定制化的AI开发监督和代码审查工具"
    our_features = [
        {"name": "GitHub Actions集成", "description": "自动运行监督检查", "category": "core"},
        {"name": "代码质量检查", "description": "检查代码复杂度和规范", "category": "core"},
        {"name": "敏感信息防护", "description": "防止敏感信息泄露", "category": "core"},
        {"name": "自动部署", "description": "功能完成后自动部署", "category": "advanced"}
    ]
    
    # 执行分析
    report = analyzer.analyze_all_competitors(our_product_description, our_features)
    
    # 保存JSON报告
    analyzer.save_report(report)
    
    # 生成Markdown报告
    md_report = analyzer.generate_markdown_report(report)
    md_path = analyzer.output_dir / "analysis_report.md"
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_report)
    print(f"📄 Markdown报告已保存到: {md_path}")


if __name__ == '__main__':
    main()
