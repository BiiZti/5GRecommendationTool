# 贡献指南

感谢您对通用套餐推荐系统的关注！我们欢迎各种形式的贡献。

## 🤝 如何贡献

### 报告问题
- 使用 [GitHub Issues](https://github.com/your-repo/issues) 报告 Bug
- 提供详细的问题描述和复现步骤
- 包含您的环境信息（Python版本、操作系统等）

### 功能建议
- 在 Issues 中提出新功能建议
- 详细描述功能的用途和实现思路
- 说明该功能如何改善用户体验

### 代码贡献

#### 开发环境设置
```bash
# 1. Fork 并克隆项目
git clone https://github.com/your-username/5GRecommendationTool.git
cd 5GRecommendationTool

# 2. 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. 运行测试
python -m pytest tests/

# 4. 检查代码质量
python run_quality_assessment.py
```

#### 代码标准
- 遵循 PEP 8 代码风格
- 使用类型注解 (Type Hints)
- 编写完整的文档字符串
- 函数长度不超过 30 行
- 最大嵌套深度不超过 3 层

#### 提交规范
```
类型(范围): 简短描述

详细描述...

Fixes #issue_number
```

类型包括：
- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 其他改动

### 数据源扩展
我们欢迎添加新的运营商数据源：

1. 继承 `DataSource` 抽象类
2. 实现 `get_packages()` 方法
3. 确保数据格式符合规范
4. 添加相应的测试用例

### 算法改进
推荐算法改进建议：

1. 机器学习集成
2. 用户行为分析
3. 个性化推荐
4. 实时数据更新

## 📝 开发者资源

### 项目架构
```
核心模块：
- recommendation_engine.py: 推荐算法核心
- data_sources.py: 数据源管理
- api_server.py: REST API 服务

应用层：
- gui.py: 图形界面应用
- api_client_example.py: API 使用示例
```

### 测试指南
- 单元测试：`tests/unit/`
- 集成测试：`tests/integration/`
- API测试：`tests/api/`
- 覆盖率要求：>85%

### 性能要求
- 推荐响应时间 < 100ms
- API 接口响应时间 < 200ms
- 内存使用 < 100MB

## 🎯 路线图

### 短期目标 (1-2个月)
- [ ] 完善测试覆盖
- [ ] 添加性能基准测试
- [ ] 改进错误处理
- [ ] 优化代码结构

### 中期目标 (3-6个月)
- [ ] 机器学习算法集成
- [ ] Web界面开发
- [ ] 数据库支持
- [ ] 缓存机制

### 长期目标 (6-12个月)
- [ ] 微服务架构
- [ ] 多语言支持
- [ ] 实时推荐
- [ ] 企业级功能

## 💬 交流沟通

- GitHub Issues: 技术讨论和问题报告
- Pull Requests: 代码审查和功能提交
- 邮箱: your-email@example.com

## 📄 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE) 文件。

感谢您的贡献！🎉 