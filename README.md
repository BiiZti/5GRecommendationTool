# 通用套餐推荐系统

## 项目简介

这是一个**高度模块化、可扩展**的套餐推荐系统，基于数学评分算法提供精准的产品推荐服务。系统采用模块化设计，支持多运营商数据源，可通过GUI界面或REST API接口使用，具有很强的复用性和扩展性。

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)](tests/)
[![Code Quality](https://img.shields.io/badge/Code%20Quality-7.75%2F10-yellow)](quality_assessment_report_20250617_030121.json)
[![API](https://img.shields.io/badge/API-REST-orange)](API_DOCUMENTATION.md)

## 🌟 核心特性

### 📦 高度模块化设计
- **推荐引擎模块**：独立的通用推荐算法，可复用于各种推荐场景
- **数据源管理**：抽象数据源接口，支持多运营商扩展
- **API服务层**：标准REST API，支持多种客户端接入
- **配置系统**：JSON配置文件，灵活调整算法参数

### 🔌 多种使用方式
- **GUI桌面应用**：基于tkinter的图形界面，开箱即用
- **REST API服务**：完整的HTTP API，支持Web集成
- **Python模块**：可作为第三方库导入使用
- **命令行工具**：支持批量处理和自动化

### 🎯 智能推荐算法
- **多维度评分**：综合考虑功能匹配度和价格优势
- **个性化分析**：基于用户具体需求生成推荐理由
- **失败分析**：当无匹配结果时提供详细原因和建议
- **可配置权重**：支持调整算法参数以适应不同场景

### 🚀 扩展性强
- **数据源扩展**：支持JSON文件、数据库、API等多种数据源
- **运营商扩展**：可轻松添加联通、电信等其他运营商
- **算法扩展**：模块化设计便于集成机器学习算法
- **UI扩展**：可基于API开发Web、移动端等多种界面

## 🏗️ 系统架构

### 分层架构设计
```
┌─────────────────┬─────────────────┬─────────────────┐
│   用户界面层     │     服务接口层   │    应用扩展层     │
│                │                │                │
│  • GUI应用      │  • REST API    │  • Web应用      │
│  • 命令行工具    │  • HTTP服务    │  • 移动应用      │
│  • 脚本接口      │  • 批量接口    │  • 第三方集成    │
└─────────────────┼─────────────────┼─────────────────┘
                 │                │
┌─────────────────┼─────────────────┼─────────────────┐
│            核心业务逻辑层           │   配置管理层     │
│                                  │                │
│  • 推荐引擎 (recommendation_engine) │  • 参数配置      │
│  • 评分算法                        │  • 权重调整      │
│  • 匹配分析                        │  • 阈值设置      │
│  • 结果排序                        │  • 验证规则      │
└─────────────────┬─────────────────┼─────────────────┘
                 │                │
┌─────────────────┼─────────────────┼─────────────────┐
│            数据访问层              │    扩展接口层     │
│                                  │                │
│  • 数据源管理 (data_sources)        │  • 插件系统      │
│  • 多运营商支持                     │  • 自定义算法     │
│  • JSON/数据库接口                  │  • 外部API      │
│  • 数据验证                        │  • 数据导入      │
└─────────────────────────────────────┴─────────────────┘
```

### 核心技术栈
- **推荐引擎**：Python + 数学建模
- **API服务**：Flask + RESTful架构
- **数据管理**：抽象工厂模式 + JSON
- **GUI界面**：tkinter (无额外依赖)
- **配置系统**：JSON配置文件
- **扩展性**：面向对象 + 抽象接口

## 安装和运行

### 环境要求
- Python 3.7+
- pip

### 快速启动（推荐）

1. 运行 `scripts/start_gui.bat` 启动GUI
2. 运行 `scripts/start_api.bat` 启动API
3. 运行 `scripts/start.bat` 启动全部服务

### 开发环境搭建

```bash
# 1. 克隆项目
git clone https://github.com/your-username/5GRecommendationTool.git
cd 5GRecommendationTool

# 2. 安装基础依赖
pip install -r requirements.txt

# 3. 安装开发依赖（可选）
pip install -r requirements-dev.txt

# 4. 运行测试
python -m pytest tests/ -v

# 5. 检查代码质量
python run_quality_assessment.py

# 6. 启动API服务
python api_server.py
```

### 手动启动

```bash
# 安装依赖
pip install -r requirements.txt

# 运行套餐推荐GUI
python gui.py

# 运行API服务器
python api_server.py
```

## 🧪 测试

项目包含完整的测试套件，确保代码质量和功能正确性。

### 运行所有测试
```bash
python -m pytest tests/ -v
```

### 生成覆盖率报告
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

### 运行特定测试
```bash
# 测试推荐引擎
python -m pytest tests/test_recommendation_engine.py -v

# 测试API服务器
python -m pytest tests/test_api_server.py -v

# 测试数据源
python -m pytest tests/test_data_sources.py -v
```

## 📊 API文档

系统提供完整的REST API接口，详见 [API文档](API_DOCUMENTATION.md)。

### 主要接口

- `GET /api/health` - 健康检查
- `GET /api/carriers` - 获取运营商列表
- `GET /api/packages` - 获取套餐列表
- `POST /api/recommend` - 套餐推荐
- `POST /api/recommend/batch` - 批量推荐

### 快速测试API

```bash
# 健康检查
curl http://127.0.0.1:5000/api/health

# 获取推荐
curl -X POST http://127.0.0.1:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"data": 30, "calls": 500, "budget": 150}'
```

## 使用指南

### 基本使用步骤

1. **启动应用**：运行`scripts/start_gui.bat`或运行`python gui.py`
2. **输入需求**：在左侧面板填写您的需求：
   - 每月流量需求 (GB)
   - 每月通话时长 (分钟)
   - 预算范围 (元/月)
3. **获取推荐**：点击"🚀 开始推荐"按钮
4. **查看结果**：在右侧推荐结果区域查看推荐结果

### 功能特色

#### 🎯 推荐系统核心
- ✅ **智能推荐** - 多维度评分算法
- ✅ **精准匹配** - 基于需求的个性化推荐
- ✅ **预算控制** - 严格的价格范围筛选
- ✅ **性价比分析** - 自动计算套餐性价比

#### 💻 多种使用方式
- ✅ **桌面GUI应用** - 直观的图形界面
- ✅ **REST API服务** - 支持Web集成
- ✅ **Python模块** - 直接代码调用

#### 🔧 技术特性
- ✅ **模块化架构** - 高度可复用的设计
- ✅ **配置驱动** - JSON配置文件支持
- ✅ **类型安全** - 完整的类型注解
- ✅ **一键启动** - 自动环境检测和依赖安装

## 📁 项目结构

```
RecommendationSystem/
├── 🎯 核心模块
│   ├── recommendation_engine.py    # 通用推荐引擎
│   ├── data_sources.py            # 数据源管理器
│   └── api_server.py              # REST API服务器
│
├── 🖥️ 用户界面
│   ├── gui.py                     # GUI桌面应用
│   └── api_client_example.py      # API客户端示例
│
├── 🧪 测试套件
│   ├── tests/__init__.py          # 测试包初始化
│   ├── tests/test_recommendation_engine.py  # 推荐引擎测试
│   ├── tests/test_data_sources.py           # 数据源测试
│   └── tests/test_api_server.py             # API测试
│
├── ⚙️ 配置和数据
│   ├── config.json                # 系统配置文件
│   ├── requirements.txt           # 项目依赖
│   ├── requirements-dev.txt       # 开发依赖
│   ├── pyproject.toml            # 现代Python项目配置
│   └── start.bat                  # 快速启动脚本
│
├── 📚 文档
│   ├── README.md                  # 项目说明
│   ├── API_DOCUMENTATION.md       # API接口文档
│   ├── CONTRIBUTING.md           # 贡献指南
│   └── LICENSE                   # 开源协议
│
└── 🔧 开发工具
    ├── .gitignore                # Git忽略文件
    ├── run_quality_assessment.py # 代码质量评估
    └── code_standards.py         # 代码标准检查
```

### 模块说明

#### 核心引擎模块
- **`recommendation_engine.py`**：可复用的推荐算法核心，支持多种产品推荐
- **`data_sources.py`**：抽象数据源管理，支持多运营商扩展
- **`api_server.py`**：标准REST API服务，支持Web集成

#### 应用层模块
- **`gui.py`**：套餐推荐图形界面应用
- **`api_client_example.py`**：API使用示例，演示如何集成

## 数据说明

### 套餐数据
项目采用[中国移动官方真实套餐数据](http://www.y576.com/aricle.asp?id=48)，包含26个不同类型套餐：

**💳 互联网卡套餐（4个）**
- 花卡宝藏版：19-39元价位，适合年轻用户

**📱 4G套餐（9个）** 
- 自由选套餐：8-38元，按需付费模式
- 飞享套餐：18-58元，流量通话均衡
- 节节高套餐：19-39元，逐月递增流量

**🚀 5G套餐（10个）**
- 5G智享套餐：128-298元，高速5G网络
- 5G全家享套餐：99-319元，全家共享

**🌟 其他套餐（3个）**
- 全球通畅享套餐：128-238元，融合宽带服务

### 推荐算法逻辑
1. **基础匹配**：流量和通话时长是否满足需求
2. **价格评估**：是否在预算范围内
3. **浪费控制**：避免推荐明显超出需求的套餐
4. **性价比计算**：每元对应的流量和通话时长
5. **综合评分**：70%功能匹配 + 30%价格因素

## 界面预览

### 📱 套餐推荐界面
- **左侧**：需求输入面板，包含流量、通话、预算输入框
- **右侧**：结果展示区域，显示推荐套餐详情
- **推荐结果**：最多10个推荐套餐，突出最佳推荐（🌟标识）
- **性价比标签**：高性价比💎、性价比良好👍、标准价格⭐

## 扩展功能

### 可以扩展的功能
- [ ] 用户偏好记忆功能
- [ ] 套餐使用历史分析
- [ ] 更多运营商数据接入
- [ ] 套餐详细信息查询
- [ ] 导出推荐结果
- [ ] 多语言支持

### 数据源扩展
- [ ] 接入中国移动官方API实时更新
- [ ] 增加更多运营商数据对比
- [ ] 用户评价数据整合
- [ ] 地区特色套餐支持

## 系统要求

### 最低配置
- **操作系统**：Windows 7+, macOS 10.12+, Linux
- **Python版本**：3.7或更高
- **内存**：512MB RAM
- **存储空间**：50MB可用空间

### 推荐配置
- **操作系统**：Windows 10+, macOS 10.15+, Ubuntu 18.04+
- **Python版本**：3.8或更高
- **内存**：1GB RAM
- **存储空间**：100MB可用空间

## 常见问题

### Q: 应用启动失败怎么办？
A: 请确保已安装Python 3.7+，并检查是否有防火墙或杀毒软件阻止运行。

### Q: 如何添加新的套餐数据？
A: 编辑`gui.py`文件中的`PACKAGES_DATA`字典，按现有格式添加新套餐。

### Q: 推荐结果不准确？
A: 推荐算法基于价格、流量、通话时长等因素。如需调整，可修改算法权重参数。

## 🤝 贡献指南

我们欢迎各种形式的贡献！请查看 [贡献指南](CONTRIBUTING.md) 了解详细信息。

### 快速贡献步骤

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 开发规范

- 遵循 PEP 8 代码风格
- 添加必要的测试用例
- 更新相关文档
- 确保所有测试通过

## 📈 质量评估

项目使用自动化质量评估系统，定期生成质量报告：

```bash
# 运行完整质量评估
python run_quality_assessment.py

# 查看最新评估报告
cat quality_assessment_report_*.json
```


## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。

## 🙏 致谢

感谢所有为项目做出贡献的开发者！

- 套餐数据来源：[中国移动官方](http://www.y576.com/aricle.asp?id=48)
- 开源社区的宝贵建议和反馈

## 📞 联系我们

- **GitHub Issues**: [报告问题](https://github.com/your-username/5GRecommendationTool/issues)
- **Pull Requests**: [贡献代码](https://github.com/your-username/5GRecommendationTool/pulls)

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！
