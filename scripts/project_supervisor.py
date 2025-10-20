#!/usr/bin/env python3
# project_supervisor.py
class ProjectSpecificSupervisor:
    def __init__(self, project_type):
        self.project_type = project_type
        self.templates = {
            'web_app': self._web_app_template(),
            'mobile_app': self._mobile_app_template(),
            'api_service': self._api_service_template(),
            'desktop_app': self._desktop_app_template()
        }
    
    def _web_app_template(self):
        return {
            'must_have': ['用户认证系统', '数据CRUD操作', '文件上传', '响应式设计', 'SEO优化'],
            'backend_required': ['RESTful API', '数据库模型', '中间件', '安全防护'],
            'frontend_required': ['路由系统', '状态管理', 'UI组件库', '错误处理'],
            'deployment': ['Docker配置', 'CI/CD流水线', '监控日志']
        }
    
    def _mobile_app_template(self):
        return {
            'must_have': ['用户引导', '数据同步', '离线功能', '推送通知', '应用内购买'],
            'platform_specific': ['iOS审核要求', 'Android发布检查'],
            'performance': ['启动优化', '内存管理', '电池优化']
        }
    
    def _api_service_template(self):
        return {
            'must_have': ['API文档', '认证授权', '速率限制', '版本控制', '错误处理'],
            'backend_required': ['数据验证', '日志记录', '监控告警', '缓存策略'],
            'deployment': ['容器化', '负载均衡', '健康检查']
        }
    
    def _desktop_app_template(self):
        return {
            'must_have': ['安装程序', '自动更新', '崩溃报告', '用户设置', '多平台支持'],
            'platform_specific': ['Windows签名', 'macOS公证', 'Linux打包'],
            'performance': ['启动时间', '内存占用', '响应速度']
        }

if __name__ == "__main__":
    supervisor = ProjectSpecificSupervisor('web_app')
    print("Web App Template:", supervisor.templates['web_app'])

