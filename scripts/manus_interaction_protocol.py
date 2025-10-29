#!/usr/bin/env python3
# manus_interaction_protocol.py
from datetime import datetime, timedelta

class ManusInteractionProtocol:
    def __init__(self):
        self.strict_mode = True
        self.required_acknowledgement = True
        
    def _calculate_deadline(self, requirements):
        """根据需求复杂度计算截止时间"""
        complexity = requirements.get('complexity', 'medium')
        hours = {'low': 4, 'medium': 8, 'high': 24}.get(complexity, 8)
        deadline = datetime.now() + timedelta(hours=hours)
        return deadline.strftime('%Y-%m-%d %H:%M')
    
    def _format_requirements(self, requirements):
        """格式化需求列表"""
        formatted = []
        for key, value in requirements.items():
            if isinstance(value, list):
                formatted.append(f"- {key}:")
                for item in value:
                    formatted.append(f"  • {item}")
            else:
                formatted.append(f"- {key}: {value}")
        return '\n'.join(formatted)
        
    def send_development_directive(self, task_description, requirements):
        """发送开发指令给Manus"""
        directive = f"""
🧠 AI PM 开发指令
==================

任务: {task_description}
优先级: 🔴 高
截止时间: {self._calculate_deadline(requirements)}

具体要求:
{self._format_requirements(requirements)}

验收标准:
✅ 功能完整实现
✅ 代码通过所有测试
✅ 文档更新完成
✅ 安全审查通过

请确认接收并立即开始执行。
"""
        return directive
    
    def enforce_completion(self, incomplete_work):
        """强制完成不完整的工作"""
        intervention = f"""
🚨 PM 强制完成指令
==================

检测到未完成工作:
{incomplete_work}

立即要求:
1. 暂停所有新功能开发
2. 优先完成上述缺失部分
3. 在4小时内提交完成版本
4. 准备代码审查会议

不遵守将触发升级处理。
"""
        return intervention

if __name__ == "__main__":
    protocol = ManusInteractionProtocol()
    
    # 示例使用
    requirements = {
        'complexity': 'medium',
        'features': ['用户认证', 'API集成', '数据验证'],
        'tests': ['单元测试', '集成测试']
    }
    
    directive = protocol.send_development_directive(
        "实现用户管理系统",
        requirements
    )
    print(directive)

