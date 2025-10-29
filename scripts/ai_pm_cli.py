#!/usr/bin/env python3
"""
AI PM CLI - 智能竞品分析命令行工具
集成竞品采集、分析和建议生成功能
"""

import argparse
import sys
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from competitor_collector import CompetitorCollector
from competitor_analyzer import CompetitorAnalyzer


def cmd_discover(args):
    """发现竞品命令"""
    print("🔍 竞品发现功能")
    collector = CompetitorCollector(data_dir=args.data_dir)
    
    competitors = collector.discover_competitors(
        product_description=args.description,
        keywords=args.keywords.split(',') if args.keywords else []
    )
    
    print(f"\n发现的竞品:")
    for i, comp in enumerate(competitors, 1):
        print(f"  {i}. {comp}")


def cmd_collect(args):
    """采集竞品信息命令"""
    print("📊 竞品信息采集")
    collector = CompetitorCollector(data_dir=args.data_dir)
    
    if args.config:
        # 从配置文件读取
        import json
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
        competitors = collector.collect_batch(config)
    else:
        # 单个竞品采集
        competitor = collector.collect_competitor_info(
            name=args.name,
            website=args.website,
            github_repo=args.github
        )
        collector.save_competitor(competitor)
        competitors = [competitor]
    
    print(f"\n✅ 成功采集 {len(competitors)} 个竞品的信息")


def cmd_analyze(args):
    """分析竞品命令"""
    print("🧠 竞品智能分析")
    analyzer = CompetitorAnalyzer(
        data_dir=args.data_dir,
        output_dir=args.output_dir
    )
    
    # 定义我们的产品
    our_product_description = args.our_description or "AI PM监督系统 - 定制化的AI开发监督和代码审查工具"
    
    # 定义我们的功能
    our_features = [
        {"name": "GitHub Actions集成", "description": "自动运行监督检查", "category": "core"},
        {"name": "代码质量检查", "description": "检查代码复杂度和规范", "category": "core"},
        {"name": "敏感信息防护", "description": "防止敏感信息泄露", "category": "core"},
        {"name": "自动部署", "description": "功能完成后自动部署", "category": "advanced"},
        {"name": "主动问题发现", "description": "自动发现代码中的潜在问题", "category": "advanced"}
    ]
    
    # 执行分析
    report = analyzer.analyze_all_competitors(our_product_description, our_features)
    
    # 保存报告
    analyzer.save_report(report, filename=args.output)
    
    # 生成Markdown报告
    if args.markdown:
        md_report = analyzer.generate_markdown_report(report)
        md_path = Path(args.output_dir) / args.output.replace('.json', '.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_report)
        print(f"📄 Markdown报告: {md_path}")


def cmd_report(args):
    """查看分析报告命令"""
    print("📄 查看分析报告")
    
    import json
    report_path = Path(args.output_dir) / args.report
    
    if not report_path.exists():
        print(f"❌ 报告文件不存在: {report_path}")
        return
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    print(f"\n分析时间: {report['analysis_date']}")
    print(f"竞品数量: {report['competitors_analyzed']}")
    print(f"功能差距: {report['total_gaps']}")
    print(f"迭代建议: {report['total_suggestions']}")
    print(f"高优先级: {report['high_priority_suggestions']}")
    
    if args.suggestions:
        print(f"\n🎯 高优先级建议 (前{args.suggestions}条):")
        for i, sugg in enumerate(report['suggestions'][:args.suggestions], 1):
            print(f"\n{i}. {sugg['title']}")
            print(f"   来源: {sugg['source_competitor']}")
            print(f"   优先级: {sugg['priority']}/5")
            print(f"   影响: {sugg['impact']} | 难度: {sugg['effort']}")
            print(f"   描述: {sugg['description']}")


def cmd_list(args):
    """列出已采集的竞品"""
    print("📋 已采集的竞品")
    collector = CompetitorCollector(data_dir=args.data_dir)
    
    competitors = collector.list_competitors()
    
    if not competitors:
        print("   (暂无数据)")
        return
    
    print(f"\n共 {len(competitors)} 个竞品:")
    for i, comp_id in enumerate(competitors, 1):
        competitor = collector.load_competitor(comp_id)
        if competitor:
            print(f"  {i}. {competitor.name}")
            print(f"     ID: {competitor.id}")
            print(f"     网站: {competitor.website}")
            print(f"     功能数: {len(competitor.features)}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='AI PM CLI - 智能竞品分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 发现竞品
  %(prog)s discover --description "AI代码审查工具" --keywords "ai,code review"
  
  # 采集竞品信息
  %(prog)s collect --name "CodeRabbit" --website "https://coderabbit.ai"
  
  # 批量采集
  %(prog)s collect --config competitors.json
  
  # 分析竞品
  %(prog)s analyze --markdown
  
  # 查看报告
  %(prog)s report --suggestions 5
  
  # 列出已采集的竞品
  %(prog)s list
"""
    )
    
    parser.add_argument('--data-dir', default='./data/competitors',
                       help='竞品数据目录 (默认: ./data/competitors)')
    parser.add_argument('--output-dir', default='./data/analysis',
                       help='分析输出目录 (默认: ./data/analysis)')
    
    subparsers = parser.add_subparsers(dest='command', help='子命令')
    
    # discover命令
    discover_parser = subparsers.add_parser('discover', help='发现竞品')
    discover_parser.add_argument('--description', required=True, help='产品描述')
    discover_parser.add_argument('--keywords', help='关键词（逗号分隔）')
    
    # collect命令
    collect_parser = subparsers.add_parser('collect', help='采集竞品信息')
    collect_parser.add_argument('--name', help='竞品名称')
    collect_parser.add_argument('--website', help='竞品网站')
    collect_parser.add_argument('--github', help='GitHub仓库URL')
    collect_parser.add_argument('--config', help='批量采集配置文件（JSON）')
    
    # analyze命令
    analyze_parser = subparsers.add_parser('analyze', help='分析竞品')
    analyze_parser.add_argument('--our-description', help='我们产品的描述')
    analyze_parser.add_argument('--output', default='analysis_report.json',
                               help='输出文件名 (默认: analysis_report.json)')
    analyze_parser.add_argument('--markdown', action='store_true',
                               help='同时生成Markdown报告')
    
    # report命令
    report_parser = subparsers.add_parser('report', help='查看分析报告')
    report_parser.add_argument('--report', default='analysis_report.json',
                              help='报告文件名 (默认: analysis_report.json)')
    report_parser.add_argument('--suggestions', type=int, default=5,
                              help='显示建议数量 (默认: 5)')
    
    # list命令
    list_parser = subparsers.add_parser('list', help='列出已采集的竞品')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 执行对应的命令
    commands = {
        'discover': cmd_discover,
        'collect': cmd_collect,
        'analyze': cmd_analyze,
        'report': cmd_report,
        'list': cmd_list
    }
    
    try:
        commands[args.command](args)
    except Exception as e:
        print(f"\n❌ 执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
