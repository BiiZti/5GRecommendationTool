"""
通用套餐推荐系统 - 统一测试套件
包含所有核心模块的单元测试
"""

import pytest
import json
from unittest.mock import Mock, patch, mock_open
from grec5.recommendation_engine import RecommendationEngine
from grec5.data_sources import DataSourceManager, ChinaMobileDataSource, JSONDataSource
from grec5.api_server import RecommendationAPI


class TestRecommendationEngine:
    """推荐引擎核心测试"""
    
    def setup_method(self):
        self.engine = RecommendationEngine()
    
    def test_basic_recommendation(self):
        """测试基础推荐功能"""
        # patch DataSourceManager 在正确模块
        with patch('grec5.data_sources.DataSourceManager') as mock_manager:
            mock_packages = [
                {
                    'name': '测试套餐',
                    'specs': {'data': 30, 'calls': 500, 'price': 100},
                    'description': '测试套餐'
                }
            ]
            mock_manager.return_value.get_all_packages.return_value = mock_packages
            # 推荐方法名为 recommend
            recommendations = self.engine.recommend({'data': 30, 'calls': 500}, 150, mock_packages)
            assert len(recommendations) > 0
            assert all('score' in rec for rec in recommendations)
    
    def test_no_match_scenario(self):
        """测试无匹配场景"""
        with patch('grec5.data_sources.DataSourceManager') as mock_manager:
            mock_manager.return_value.get_all_packages.return_value = []
            recommendations = self.engine.recommend({'data': 30, 'calls': 500}, 150, [])
            assert len(recommendations) == 0
    
    def test_score_calculation(self):
        """测试评分计算"""
        user_needs = {'data': 30, 'calls': 500}
        product_specs = {'data': 30, 'calls': 500, 'price': 100}
        score = self.engine.calculate_usage_score(user_needs, product_specs)
        assert score >= 0


class TestDataSources:
    """数据源管理测试"""
    
    def test_china_mobile_data(self):
        """测试中国移动数据源"""
        source = ChinaMobileDataSource()
        packages = source.get_packages()
        
        assert len(packages) > 0
        assert all('name' in pkg for pkg in packages)
        assert all('specs' in pkg for pkg in packages)
        assert all('price' in pkg['specs'] for pkg in packages)
    
    def test_data_manager(self):
        """测试数据管理器"""
        manager = DataSourceManager()
        
        # 测试获取所有套餐
        packages = manager.get_all_packages()
        assert len(packages) > 0
        
        # 测试按运营商获取
        mobile_packages = manager.get_packages_by_carrier('中国移动')
        assert len(mobile_packages) > 0
    
    @patch('builtins.open', new_callable=mock_open, read_data='[{"name": "测试", "specs": {"data": 30, "calls": 500, "price": 100}, "type": "测试", "description": "测试", "carrier": "测试运营商"}]')
    def test_json_data_source(self, mock_file):
        """测试JSON数据源"""
        source = JSONDataSource('test.json', '测试运营商')
        packages = source.get_packages()
        
        assert len(packages) == 1
        assert packages[0]['name'] == '测试'


class TestAPIServer:
    """API服务器测试"""
    
    def setup_method(self):
        self.api = RecommendationAPI()
        self.api.app.config['TESTING'] = True
        self.client = self.api.app.test_client()
    
    def test_health_check(self):
        """测试健康检查"""
        response = self.client.get('/api/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'ok'
    
    def test_get_carriers(self):
        """测试获取运营商"""
        response = self.client.get('/api/carriers')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
        assert '中国移动' in data['data']
    
    def test_get_packages(self):
        """测试获取套餐"""
        response = self.client.get('/api/packages')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
        assert len(data['data']) > 0
    
    @patch('grec5.recommendation_engine.RecommendationEngine.recommend', return_value=[{'product': {'name': '测试套餐', 'specs': {'data': 30, 'calls': 500, 'price': 100}}, 'score': 8.5, 'usage_score': 1.0, 'price_score': 1.0, 'match_reason': '测试理由'}])
    def test_recommendation_api(self, mock_recommend):
        """测试推荐API"""
        request_data = {'user_needs': {'data': 30, 'calls': 500}, 'user_budget': 150}
        response = self.client.post('/api/recommend',
                                  data=json.dumps(request_data),
                                  content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert isinstance(data['data'], list)
    
    def test_error_handling(self):
        """测试错误处理"""
        # 测试缺少参数
        response = self.client.post('/api/recommend',
                                  data=json.dumps({}),
                                  content_type='application/json')
        assert response.status_code == 400
        
        # 测试无效JSON
        response = self.client.post('/api/recommend',
                                  data='invalid json',
                                  content_type='application/json')
        assert response.status_code == 400 or response.status_code == 500


class TestIntegration:
    """集成测试"""
    
    def test_full_recommendation_flow(self):
        """测试完整推荐流程"""
        # 初始化组件
        engine = RecommendationEngine()
        data_manager = DataSourceManager()
        packages = data_manager.get_all_packages()
        
        # 执行推荐
        recommendations = engine.recommend({'data': 30, 'calls': 500}, 150, packages)
        
        # 验证结果结构
        assert isinstance(recommendations, list)
    
    def test_api_integration(self):
        """测试API集成"""
        api = RecommendationAPI()
        api.app.config['TESTING'] = True
        
        with api.app.test_client() as client:
            # 健康检查
            health_response = client.get('/api/health')
            assert health_response.status_code == 200
            
            # 获取套餐
            packages_response = client.get('/api/packages')
            assert packages_response.status_code == 200
            
            # 推荐请求
            recommend_response = client.post('/api/recommend',
                                           data=json.dumps({'user_needs': {'data': 30, 'calls': 500}, 'user_budget': 150}),
                                           content_type='application/json')
            assert recommend_response.status_code == 200 or recommend_response.status_code == 400


if __name__ == '__main__':
    # 运行所有测试
    pytest.main([__file__, '-v'])