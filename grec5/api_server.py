#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推荐系统API服务器
提供REST API接口，支持多种客户端接入
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Dict, List, Optional
import json

from .recommendation_engine import RecommendationEngine
from .data_sources import DataSourceManager
from .data_sources import validate_package_data


class RecommendationAPI:
    """推荐系统API类"""
    
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)  # 允许跨域请求
        
        self.engine = RecommendationEngine()
        self.data_manager = DataSourceManager()
        
        self._setup_routes()
    
    def _setup_routes(self):
        """设置API路由"""
        # 将路由设置拆分为更小的函数以提高可维护性
        self._setup_health_routes()
        self._setup_data_routes()
        self._setup_recommendation_routes()
        self._setup_config_routes()
        self._setup_error_handlers()
    
    def _setup_health_routes(self):
        """设置健康检查路由"""
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """健康检查接口"""
            return jsonify({
                "status": "ok",
                "message": "推荐系统API运行正常",
                "version": "1.0.0"
            })
        
    def _setup_data_routes(self):
        """设置数据相关路由"""
        @self.app.route('/api/carriers', methods=['GET'])
        def get_carriers():
            """获取支持的运营商列表"""
            try:
                carriers = self.data_manager.get_available_carriers()
                return jsonify({
                    "success": True,
                    "data": carriers,
                    "count": len(carriers)
                })
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
        @self.app.route('/api/packages', methods=['GET'])
        def get_packages():
            """获取套餐列表"""
            try:
                carrier = request.args.get('carrier')
                
                if carrier:
                    packages = self.data_manager.get_packages_by_carrier(carrier)
                else:
                    packages = self.data_manager.get_all_packages()
                
                return jsonify({
                    "success": True,
                    "data": packages,
                    "count": len(packages)
                })
            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500
        
    def _setup_recommendation_routes(self):
        """设置推荐相关路由"""
        @self.app.route('/api/recommend', methods=['POST'])
        def recommend():
            """推荐接口"""
            return self._handle_single_recommendation()
        
        @self.app.route('/api/batch-recommend', methods=['POST'])
        def batch_recommend():
            """批量推荐接口"""
            return self._handle_batch_recommendation()
    
    def _handle_single_recommendation(self):
        """处理单个推荐请求"""
        try:
            request_data = request.get_json()
            
            # 验证必需参数
            validation_error = self._validate_recommendation_request(request_data)
            if validation_error:
                return validation_error
            
            user_needs = request_data['user_needs']
            user_budget = request_data['user_budget']
            carrier_filter = request_data.get('carrier')
            
            # 获取套餐数据
            packages = self._get_packages_for_recommendation(carrier_filter)
            
            # 生成推荐
            recommendations = self.engine.recommend(user_needs, user_budget, packages)
            
            # 如果没有推荐结果，提供分析
            if not recommendations:
                analysis = self.engine.analyze_no_match_reason(
                    user_needs, user_budget, packages
                )
                return jsonify({
                    "success": True,
                    "data": [],
                    "analysis": analysis,
                    "message": "没有找到符合需求的套餐"
                })
            
            return jsonify({
                "success": True,
                "data": recommendations,
                "count": len(recommendations)
            })
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    def _validate_recommendation_request(self, request_data):
        """验证推荐请求参数"""
        if not request_data:
            return jsonify({
                "success": False,
                "error": "请求数据为空"
            }), 400
        
        required_fields = ['user_needs', 'user_budget']
        for field in required_fields:
            if field not in request_data:
                return jsonify({
                    "success": False,
                    "error": f"缺少必需参数: {field}"
                }), 400
        return None
    
    def _get_packages_for_recommendation(self, carrier_filter):
        """获取用于推荐的套餐数据"""
        if carrier_filter:
            return self.data_manager.get_packages_by_carrier(carrier_filter)
        else:
            return self.data_manager.get_all_packages()
        
    def _handle_batch_recommendation(self):
        """处理批量推荐请求"""
        try:
            request_data = request.get_json()
            
            if 'requests' not in request_data:
                return jsonify({
                    "success": False,
                    "error": "缺少requests参数"
                }), 400
            
            requests_list = request_data['requests']
            results = []
            
            packages = self.data_manager.get_all_packages()
            
            for single_request in requests_list:
                if 'user_needs' not in single_request or 'user_budget' not in single_request:
                    results.append({
                        "success": False,
                        "error": "请求缺少必需参数"
                    })
                    continue
                
                recommendations = self.engine.recommend(
                    single_request['user_needs'], 
                    single_request['user_budget'], 
                    packages
                )
                
                results.append({
                    "success": True,
                    "data": recommendations,
                    "count": len(recommendations)
                })
            
            return jsonify({
                "success": True,
                "results": results
            })
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
        
    def _setup_config_routes(self):
        """设置配置相关路由"""
        @self.app.route('/api/config', methods=['GET'])
        def get_config():
            """获取推荐引擎配置"""
            return jsonify({
                "success": True,
                "data": self.engine.config
            })
        
        @self.app.route('/api/config', methods=['PUT'])
        def update_config():
            """更新推荐引擎配置"""
            return self._handle_config_update()
        
        @self.app.route('/api/validate', methods=['POST'])
        def validate_data():
            """验证数据格式"""
            return self._handle_data_validation()
    
    def _handle_config_update(self):
        """处理配置更新"""
        try:
            request_data = request.get_json()
            
            # 更新配置
            if 'score_weights' in request_data:
                self.engine.config['score_weights'].update(request_data['score_weights'])
            
            if 'thresholds' in request_data:
                self.engine.config['thresholds'].update(request_data['thresholds'])
            
            if 'max_recommendations' in request_data:
                self.engine.config['max_recommendations'] = request_data['max_recommendations']
            
            return jsonify({
                "success": True,
                "message": "配置更新成功",
                "data": self.engine.config
            })
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    def _handle_data_validation(self):
        """处理数据验证"""
        try:
            request_data = request.get_json()
            
            if 'packages' not in request_data:
                return jsonify({
                    "success": False,
                    "error": "缺少packages参数"
                }), 400
            
            validation_errors = validate_package_data(request_data['packages'])
            
            return jsonify({
                "success": True,
                "valid": len(validation_errors) == 0,
                "errors": validation_errors
            })
            
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    def _setup_error_handlers(self):
        """设置错误处理器"""
        @self.app.errorhandler(404)
        def not_found(error):
            """404错误处理"""
            return jsonify({
                "success": False,
                "error": "API接口不存在"
            }), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            """500错误处理"""
            return jsonify({
                "success": False,
                "error": "服务器内部错误"
            }), 500
    
    def run(self, host='127.0.0.1', port=5000, debug=False):
        """启动API服务器"""
        print(f"🚀 推荐系统API服务器启动")
        print(f"📡 地址: http://{host}:{port}")
        print(f"📋 API文档:")
        print(f"   GET  /api/health          - 健康检查")
        print(f"   GET  /api/carriers        - 获取运营商列表")
        print(f"   GET  /api/packages        - 获取套餐列表")
        print(f"   POST /api/recommend       - 获取推荐")
        print(f"   POST /api/batch-recommend - 批量推荐")
        print(f"   GET  /api/config          - 获取配置")
        print(f"   PUT  /api/config          - 更新配置")
        print(f"   POST /api/validate        - 验证数据")
        
        self.app.run(host=host, port=port, debug=debug)


def create_sample_client():
    """创建示例客户端代码"""
    client_generator = SampleClientGenerator()
    client_generator.generate_sample_file()


class SampleClientGenerator:
    """示例客户端代码生成器"""
    
    def __init__(self, api_base_url: str = "http://127.0.0.1:5000/api"):
        self.api_base_url = api_base_url
    
    def generate_sample_file(self) -> None:
        """生成示例客户端文件"""
        sample_code = self._create_sample_code()
        self._write_to_file(sample_code)
        print("✅ 已生成API客户端示例: api_client_example.py")
    
    def _create_sample_code(self) -> str:
        """创建示例代码内容"""
        return f'''
# 推荐系统API客户端示例
import requests
import json

API_BASE_URL = "{self.api_base_url}"

{self._get_health_check_code()}

{self._get_carriers_list_code()}

{self._get_recommendation_code()}

{self._get_batch_recommendation_code()}
'''
    
    def _get_health_check_code(self) -> str:
        """获取健康检查代码"""
        return '''# 1. 健康检查
response = requests.get(f"{API_BASE_URL}/health")
print("健康检查:", response.json())'''
    
    def _get_carriers_list_code(self) -> str:
        """获取运营商列表代码"""
        return '''# 2. 获取运营商列表
response = requests.get(f"{API_BASE_URL}/carriers")
print("运营商列表:", response.json())'''
    
    def _get_recommendation_code(self) -> str:
        """获取推荐代码"""
        return '''# 3. 获取推荐
recommend_data = {
    "user_needs": {
        "data": 30,
        "calls": 500
    },
    "user_budget": 150
}

response = requests.post(
    f"{API_BASE_URL}/recommend",
    headers={"Content-Type": "application/json"},
    data=json.dumps(recommend_data)
)
print("推荐结果:", response.json())'''
    
    def _get_batch_recommendation_code(self) -> str:
        """获取批量推荐代码"""
        return '''# 4. 批量推荐
batch_data = {
    "requests": [
        {
            "user_needs": {"data": 20, "calls": 300},
            "user_budget": 100
        },
        {
            "user_needs": {"data": 50, "calls": 800},
            "user_budget": 200
        }
    ]
}

response = requests.post(
    f"{API_BASE_URL}/batch-recommend",
    headers={"Content-Type": "application/json"},
    data=json.dumps(batch_data)
)
print("批量推荐结果:", response.json())'''
    
    def _write_to_file(self, content: str) -> None:
        """写入文件"""
        with open('api_client_example.py', 'w', encoding='utf-8') as client_file:
            client_file.write(content)


if __name__ == "__main__":
    # 创建并启动API服务器
    api = RecommendationAPI()
    
    # 生成示例客户端代码
    create_sample_client()
    
    # 启动服务器
    api.run(debug=True) 