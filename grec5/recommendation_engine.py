#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通用推荐引擎模块
可复用的推荐算法核心，支持多种产品推荐场景
"""

import json
from typing import List, Dict, Any, Optional


class RecommendationEngine:
    """
    通用推荐引擎 - 基于多维度评分的推荐算法
    
    特性：
    - 支持多维度需求匹配
    - 可配置评分权重
    - 通用化设计，适用于各种推荐场景
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化推荐引擎
        
        Args:
            config: 配置参数，包含权重和阈值设置
        """
        self.config = config or self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """获取默认配置"""
        return {
            "score_weights": {
                "usage_match": 0.7,  # 使用匹配度权重
                "price_advantage": 0.3  # 价格优势权重
            },
            "thresholds": {
                "budget_tolerance": 1.2,  # 预算容忍度
                "waste_penalty": 0.1,     # 浪费惩罚系数
                "perfect_match_ratio": 1.5  # 完美匹配比例
            },
            "max_recommendations": 10
        }
    
    def calculate_usage_score(self, user_needs: Dict, product_specs: Dict) -> float:
        """
        计算使用匹配度评分
        
        Args:
            user_needs: 用户需求 {"data": 30, "calls": 500}
            product_specs: 产品规格 {"data": 40, "calls": 600}
            
        Returns:
            匹配度评分 (0-2.0)
        """
        scores = self._calculate_satisfaction_scores(user_needs, product_specs)
        penalties = self._calculate_waste_penalties(user_needs, product_specs)
        
        return self._compute_final_usage_score(scores, penalties)
    
    def _calculate_satisfaction_scores(self, user_needs: Dict, product_specs: Dict) -> List[float]:
        """计算满足度评分列表"""
        scores = []
        for need_key, user_value in user_needs.items():
            if need_key in product_specs:
                product_value = product_specs[need_key]
                if user_value > 0:
                    satisfaction = min(product_value / user_value, 2.0)
                    scores.append(satisfaction)
                else:
                    scores.append(1.0)  # 用户无需求时给予标准分
        return scores
    
    def _calculate_waste_penalties(self, user_needs: Dict, product_specs: Dict) -> List[float]:
        """计算浪费惩罚列表"""
        penalties = []
        for need_key, user_value in user_needs.items():
            if need_key in product_specs and user_value > 0:
                product_value = product_specs[need_key]
                if product_value > user_value:
                    waste_ratio = (product_value - user_value) / user_value
                    penalties.append(waste_ratio)
        return penalties
    
    def _compute_final_usage_score(self, scores: List[float], penalties: List[float]) -> float:
        """计算最终使用评分"""
        avg_score = sum(scores) / len(scores) if scores else 0
        avg_penalty = sum(penalties) / len(penalties) if penalties else 0
        
        final_score = avg_score - avg_penalty * self.config["thresholds"]["waste_penalty"]
        return max(final_score, 0)
    
    def calculate_price_score(self, user_budget: float, product_price: float) -> float:
        """
        计算价格优势评分
        
        Args:
            user_budget: 用户预算
            product_price: 产品价格
            
        Returns:
            价格评分
        """
        if product_price <= 0:
            return 0
        return user_budget / product_price
    
    def check_basic_requirements(self, user_needs: Dict, product_specs: Dict, 
                                user_budget: float, product_price: float) -> bool:
        """
        检查是否满足基本需求
        
        Args:
            user_needs: 用户需求
            product_specs: 产品规格
            user_budget: 用户预算
            product_price: 产品价格
            
        Returns:
            是否满足基本需求
        """
        # 检查价格
        if product_price > user_budget * self.config["thresholds"]["budget_tolerance"]:
            return False
        
        # 检查功能需求
        for need_key, user_value in user_needs.items():
            if need_key in product_specs:
                if product_specs[need_key] < user_value:
                    return False
        
        return True
    
    def recommend(self, user_needs: Dict, user_budget: float, 
                 products: List[Dict]) -> List[Dict]:
        """
        生成推荐结果
        
        Args:
            user_needs: 用户需求 {"data": 30, "calls": 500}
            user_budget: 用户预算
            products: 产品列表，每个产品包含规格和其他信息
            
        Returns:
            推荐结果列表，按评分排序
        """
        recommendations = []
        
        for product in products:
            recommendation = self._evaluate_single_product(user_needs, user_budget, product)
            if recommendation:
                recommendations.append(recommendation)
        
        return self._sort_and_limit_recommendations(recommendations)
    
    def _evaluate_single_product(self, user_needs: Dict, user_budget: float, 
                                product: Dict) -> Optional[Dict]:
        """评估单个产品是否推荐"""
        product_specs = product.get("specs", {})
        product_price = product_specs.get("price", product.get("price", 0))
        
        # 检查基本需求
        if not self.check_basic_requirements(user_needs, product_specs, 
                                           user_budget, product_price):
            return None
        
        # 计算评分
        usage_score = self.calculate_usage_score(user_needs, product_specs)
        price_score = self.calculate_price_score(user_budget, product_price)
        final_score = self._calculate_weighted_score(usage_score, price_score)
        
        # 生成推荐理由
        match_reason = self.generate_match_reason(user_needs, user_budget, product)
        
        return {
            "product": product,
            "score": round(final_score, 2),
            "usage_score": round(usage_score, 2),
            "price_score": round(price_score, 2),
            "match_reason": match_reason
        }
    
    def _calculate_weighted_score(self, usage_score: float, price_score: float) -> float:
        """计算加权综合评分"""
        return (usage_score * self.config["score_weights"]["usage_match"] + 
                price_score * self.config["score_weights"]["price_advantage"])
    
    def _sort_and_limit_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """排序并限制推荐数量"""
        recommendations.sort(key=lambda recommendation: recommendation["score"], reverse=True)
        return recommendations[:self.config["max_recommendations"]]
    
    def generate_match_reason(self, user_needs: Dict, user_budget: float, 
                            product: Dict) -> str:
        """
        生成推荐理由
        
        Args:
            user_needs: 用户需求
            user_budget: 用户预算
            product: 产品信息
            
        Returns:
            推荐理由文本
        """
        reasons = []
        product_specs = product.get("specs", {})
        product_price = product_specs.get("price", product.get("price", 0))
        
        # 分析需求匹配和价格优势
        need_reasons = self._analyze_need_match_reasons(user_needs, product_specs)
        price_reasons = self._analyze_price_reasons(user_budget, product_price)
        
        reasons.extend(need_reasons)
        reasons.extend(price_reasons)
        
        return "；".join(reasons)
    
    def _analyze_need_match_reasons(self, user_needs: Dict, product_specs: Dict) -> List[str]:
        """分析需求匹配的推荐理由"""
        reasons = []
        for need_key, user_value in user_needs.items():
            if need_key in product_specs:
                product_value = product_specs[need_key]
                need_name = self._get_need_display_name(need_key)
                unit = self._get_need_unit(need_key)
                
                if product_value >= user_value:
                    perfect_match_threshold = user_value * self.config["thresholds"]["perfect_match_ratio"]
                    if product_value <= perfect_match_threshold:
                        reasons.append(f"{need_name}{product_value}{unit}完全满足您{user_value}{unit}的需求")
                    else:
                        excess = product_value - user_value
                        reasons.append(f"{need_name}{product_value}{unit}充足，比需求多{excess:.1f}{unit}")
        return reasons
    
    def _analyze_price_reasons(self, user_budget: float, product_price: float) -> List[str]:
        """分析价格相关的推荐理由"""
        reasons = []
        if product_price <= user_budget:
            savings = user_budget - product_price
            if savings >= 20:
                reasons.append(f"价格{product_price}元，比预算节省{savings}元")
            else:
                reasons.append(f"价格{product_price}元，在预算范围内")
        elif product_price <= user_budget * self.config["thresholds"]["budget_tolerance"]:
            excess = product_price - user_budget
            reasons.append(f"价格{product_price}元，超预算{excess}元但性价比高")
        return reasons
    
    def _get_need_display_name(self, need_key: str) -> str:
        """获取需求的显示名称"""
        name_mapping = {
            "data": "流量",
            "calls": "通话",
            "sms": "短信"
        }
        return name_mapping.get(need_key, need_key)
    
    def _get_need_unit(self, need_key: str) -> str:
        """获取需求的单位"""
        unit_mapping = {
            "data": "GB",
            "calls": "分钟",
            "sms": "条"
        }
        return unit_mapping.get(need_key, "")
    
    def analyze_no_match_reason(self, user_needs: Dict, user_budget: float, 
                               products: List[Dict]) -> Dict:
        """
        分析无匹配结果的原因
        
        Args:
            user_needs: 用户需求
            user_budget: 用户预算
            products: 产品列表
            
        Returns:
            分析结果
        """
        analysis = {
            "over_budget_products": [],
            "insufficient_specs": {},
            "suggestions": []
        }
        
        # 分析产品不匹配的原因
        self._analyze_product_mismatch(products, user_needs, user_budget, analysis)
        
        # 生成改进建议
        self._generate_improvement_suggestions(analysis, user_needs)
        
        return analysis
    
    def _analyze_product_mismatch(self, products: List[Dict], user_needs: Dict, 
                                 user_budget: float, analysis: Dict) -> None:
        """分析产品不匹配的具体原因"""
        for product in products:
            product_specs = product.get("specs", {})
            product_price = product_specs.get("price", product.get("price", 0))
            
            # 检查是否因价格超出被排除
            if self._is_over_budget_but_specs_satisfy(product_specs, user_needs, product_price, user_budget):
                analysis["over_budget_products"].append(product)
            
            # 检查规格不足的情况
            self._check_insufficient_specs(product_specs, product_price, user_needs, user_budget, analysis, product)
    
    def _is_over_budget_but_specs_satisfy(self, product_specs: Dict, user_needs: Dict, 
                                         product_price: float, user_budget: float) -> bool:
        """检查是否规格满足但价格超出预算"""
        specs_satisfy = all(product_specs.get(key, 0) >= value for key, value in user_needs.items())
        budget_tolerance = user_budget * self.config["thresholds"]["budget_tolerance"]
        return specs_satisfy and product_price > budget_tolerance
    
    def _check_insufficient_specs(self, product_specs: Dict, product_price: float, 
                                 user_needs: Dict, user_budget: float, analysis: Dict, product: Dict) -> None:
        """检查规格不足的情况"""
        budget_tolerance = user_budget * self.config["thresholds"]["budget_tolerance"]
        if product_price <= budget_tolerance:
            for need_key, user_value in user_needs.items():
                if product_specs.get(need_key, 0) < user_value:
                    if need_key not in analysis["insufficient_specs"]:
                        analysis["insufficient_specs"][need_key] = []
                    analysis["insufficient_specs"][need_key].append(product)
    
    def _generate_improvement_suggestions(self, analysis: Dict, user_needs: Dict) -> None:
        """生成改进建议"""
        # 价格相关建议
        if analysis["over_budget_products"]:
            min_price = min(prod.get("specs", {}).get("price", prod.get("price", 0)) 
                          for prod in analysis["over_budget_products"])
            analysis["suggestions"].append(f"适当提高预算至{min_price}元")
        
        # 规格相关建议
        for need_key, products_list in analysis["insufficient_specs"].items():
            max_spec = max(prod.get("specs", {}).get(need_key, 0) for prod in products_list)
            need_name = self._get_need_display_name(need_key)
            unit = self._get_need_unit(need_key)
            analysis["suggestions"].append(f"降低{need_name}需求至{max_spec}{unit}")


def load_config_from_file(config_file: str) -> Dict:
    """从文件加载配置"""
    try:
        with open(config_file, 'r', encoding='utf-8') as config_file_handle:
            return json.load(config_file_handle)
    except FileNotFoundError:
        return {}


if __name__ == "__main__":
    # 示例用法
    engine = RecommendationEngine()
    
    # 示例产品数据
    products = [
        {
            "name": "产品A",
            "specs": {"data": 30, "calls": 500, "price": 100},
            "features": ["特性1", "特性2"]
        },
        {
            "name": "产品B", 
            "specs": {"data": 50, "calls": 800, "price": 150},
            "features": ["特性3", "特性4"]
        }
    ]
    
    # 用户需求
    user_needs = {"data": 25, "calls": 400}
    user_budget = 120
    
    # 获取推荐
    recommendations = engine.recommend(user_needs, user_budget, products)
    
    for i, rec in enumerate(recommendations, 1):
        print(f"推荐 #{i}: {rec['product']['name']}")
        print(f"评分: {rec['score']}")
        print(f"理由: {rec['match_reason']}")
        print("-" * 40) 