#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据源管理模块
支持多运营商套餐数据的统一管理和扩展
"""

import json
from typing import Dict, List, Optional
from abc import ABC, abstractmethod


class DataSource(ABC):
    """数据源抽象基类"""
    
    @abstractmethod
    def get_packages(self) -> List[Dict]:
        """获取套餐数据"""
        pass
    
    @abstractmethod
    def get_carrier_name(self) -> str:
        """获取运营商名称"""
        pass


class ChinaMobileDataSource(DataSource):
    """中国移动数据源"""
    
    def __init__(self):
        self.carrier_name = "中国移动"
        self._packages_data = self._load_china_mobile_packages()
    
    def get_carrier_name(self) -> str:
        """获取运营商名称"""
        return self.carrier_name
    
    def get_packages(self) -> List[Dict]:
        """获取套餐数据列表"""
        return self._packages_data
    
    def _load_china_mobile_packages(self) -> List[Dict]:
        """加载中国移动套餐数据"""
        # 将大量套餐数据拆分为更小的逻辑单元
        packages = []
        packages.extend(self._get_internet_card_packages())
        packages.extend(self._get_4g_packages())
        packages.extend(self._get_5g_packages())
        packages.extend(self._get_other_packages())
        return packages
    
    def _get_internet_card_packages(self) -> List[Dict]:
        """获取互联网卡套餐"""
        return [
            {
                "name": "花卡宝藏版19元", 
                "specs": {"data": 30, "calls": 0, "price": 19}, 
                "features": ["定向流量30GB", "亲情号免费"], 
                "type": "互联网卡",
                "carrier": self.carrier_name
            },
            {
                "name": "花卡宝藏版20元", 
                "specs": {"data": 10, "calls": 0, "price": 20}, 
                "features": ["通用流量10GB", "亲情号免费"], 
                "type": "互联网卡",
                "carrier": self.carrier_name
            },
            {
                "name": "花卡宝藏版29元", 
                "specs": {"data": 35, "calls": 0, "price": 29}, 
                "features": ["通用5GB+定向30GB", "见卡片详情"], 
                "type": "互联网卡",
                "carrier": self.carrier_name
            },
            {
                "name": "花卡宝藏版39元", 
                "specs": {"data": 40, "calls": 0, "price": 39}, 
                "features": ["通用10GB+定向30GB", "亲情号免费"], 
                "type": "互联网卡",
                "carrier": self.carrier_name
            }
        ]
    
    def _get_4g_packages(self) -> List[Dict]:
        """获取4G套餐"""
        packages = []
        packages.extend(self._get_4g_freedom_packages())
        packages.extend(self._get_4g_flight_packages())
        packages.extend(self._get_4g_growth_packages())
        return packages
    
    def _get_4g_freedom_packages(self) -> List[Dict]:
        """获取4G自由选套餐"""
        return [
            {
                "name": "4G自由选8元", 
                "specs": {"data": 0.1, "calls": 0, "price": 8}, 
                "features": ["套内资源100M", "语音0.25元/分钟"], 
                "type": "4G套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "4G自由选18元", 
                "specs": {"data": 0.3, "calls": 0, "price": 18}, 
                "features": ["套内资源300M", "语音0.19元/分钟"], 
                "type": "4G套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "4G自由选28元", 
                "specs": {"data": 0.9, "calls": 0, "price": 28}, 
                "features": ["套内资源900M", "语音0.19元/分钟"], 
                "type": "4G套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "4G自由选38元", 
                "specs": {"data": 2.7, "calls": 0, "price": 38}, 
                "features": ["套内资源2700M", "语音0.19元/分钟"], 
                "type": "4G套餐",
                "carrier": self.carrier_name
            }
        ]
    
    def _get_4g_flight_packages(self) -> List[Dict]:
        """获取4G飞享套餐"""
        return [
            {
                "name": "4G飞享18元", 
                "specs": {"data": 1, "calls": 30, "price": 18}, 
                "features": ["套内通用流量1G", "套内通话30分钟"], 
                "type": "4G套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "4G飞享38元", 
                "specs": {"data": 3, "calls": 100, "price": 38}, 
                "features": ["套内通用流量3G", "套内通话100分钟"], 
                "type": "4G套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "4G飞享58元", 
                "specs": {"data": 5, "calls": 200, "price": 58}, 
                "features": ["套内通用流量5G", "套内通话200分钟"], 
                "type": "4G套餐",
                "carrier": self.carrier_name
            }
        ]
    
    def _get_4g_growth_packages(self) -> List[Dict]:
        """获取4G节节高套餐"""
        return [
            {
                "name": "4G节节高19元", 
                "specs": {"data": 6.6, "calls": 50, "price": 19}, 
                "features": ["首月1GB逐月递增", "套内通话50分钟"], 
                "type": "4G套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "4G节节高39元", 
                "specs": {"data": 13, "calls": 100, "price": 39}, 
                "features": ["首月4GB逐月递增", "套内通话100分钟"], 
                "type": "4G套餐",
                "carrier": self.carrier_name
            }
        ]
    
    def _get_5g_packages(self) -> List[Dict]:
        """获取5G套餐"""
        packages = []
        packages.extend(self._get_5g_smart_packages())
        packages.extend(self._get_5g_family_packages())
        return packages
    
    def _get_5g_smart_packages(self) -> List[Dict]:
        """获取5G智享套餐"""
        return [
            {
                "name": "5G智享128元", 
                "specs": {"data": 30, "calls": 500, "price": 128}, 
                "features": ["5G网络", "套内通用流量30G", "套内通话500分钟"], 
                "type": "5G套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "5G智享158元", 
                "specs": {"data": 40, "calls": 700, "price": 158}, 
                "features": ["5G网络", "套内通用流量40G", "套内通话700分钟"], 
                "type": "5G套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "5G智享198元", 
                "specs": {"data": 60, "calls": 1000, "price": 198}, 
                "features": ["5G网络", "套内通用流量60G", "套内通话1000分钟"], 
                "type": "5G套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "5G智享238元", 
                "specs": {"data": 80, "calls": 1000, "price": 238}, 
                "features": ["5G网络", "套内通用流量80G", "套内通话1000分钟"], 
                "type": "5G套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "5G智享298元", 
                "specs": {"data": 100, "calls": 1500, "price": 298}, 
                "features": ["5G网络", "套内通用流量100G", "套内通话1500分钟"], 
                "type": "5G套餐",
                "carrier": self.carrier_name
            }
        ]
    
    def _get_5g_family_packages(self) -> List[Dict]:
        """获取5G全家享套餐"""
        return [
            {
                "name": "5G全家享99元", 
                "specs": {"data": 15, "calls": 300, "price": 99}, 
                "features": ["5G网络", "套内通用流量15G", "套内通话300分钟"], 
                "type": "5G套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "5G全家享139元", 
                "specs": {"data": 30, "calls": 1000, "price": 139}, 
                "features": ["5G网络", "套内通用流量30G", "套内通话1000分钟"], 
                "type": "5G套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "5G全家享169元", 
                "specs": {"data": 40, "calls": 1600, "price": 169}, 
                "features": ["5G网络", "套内通用流量40G", "套内通话1600分钟"], 
                "type": "5G套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "5G全家享219元", 
                "specs": {"data": 60, "calls": 2000, "price": 219}, 
                "features": ["5G网络", "套内通用流量60G", "套内通话2000分钟"], 
                "type": "5G套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "5G全家享319元", 
                "specs": {"data": 100, "calls": 2500, "price": 319}, 
                "features": ["5G网络", "套内通用流量100G", "套内通话2500分钟"], 
                "type": "5G套餐",
                "carrier": self.carrier_name
            }
        ]
    
    def _get_other_packages(self) -> List[Dict]:
        """获取其他套餐"""
        return [
            {
                "name": "全球通畅享128元", 
                "specs": {"data": 20, "calls": 300, "price": 128}, 
                "features": ["流量放心用20G", "国内语音300分钟", "融合宽带50M"], 
                "type": "其他套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "全球通畅享188元", 
                "specs": {"data": 30, "calls": 500, "price": 188}, 
                "features": ["流量放心用30G", "国内语音500分钟", "融合宽带100M"], 
                "type": "其他套餐",
                "carrier": self.carrier_name
            },
            {
                "name": "全球通畅享238元", 
                "specs": {"data": 40, "calls": 700, "price": 238}, 
                "features": ["流量放心用40G", "国内语音700分钟", "融合宽带200M"], 
                "type": "其他套餐",
                "carrier": self.carrier_name
            }
        ]


class ChinaUnicomDataSource(DataSource):
    """中国联通数据源（示例扩展）"""
    
    def __init__(self):
        self.carrier_name = "中国联通"
    
    def get_carrier_name(self) -> str:
        """获取运营商名称"""
        return self.carrier_name
    
    def get_packages(self) -> List[Dict]:
        """获取联通套餐数据"""
        # 这里可以扩展联通的套餐数据
        return [
            {
                "name": "联通冰激凌套餐199元",
                "specs": {"data": 40, "calls": 1000, "price": 199},
                "features": ["5G网络", "腾讯视频会员"],
                "type": "5G套餐",
                "carrier": self.carrier_name
            }
            # 可以添加更多联通套餐...
        ]


class ChinaTelecomDataSource(DataSource):
    """中国电信数据源（示例扩展）"""
    
    def __init__(self):
        self.carrier_name = "中国电信"
    
    def get_carrier_name(self) -> str:
        """获取运营商名称"""
        return self.carrier_name
    
    def get_packages(self) -> List[Dict]:
        """获取电信套餐数据"""
        # 这里可以扩展电信的套餐数据
        return [
            {
                "name": "电信5G畅享套餐129元",
                "specs": {"data": 30, "calls": 500, "price": 129},
                "features": ["5G网络", "天翼云盘"],
                "type": "5G套餐",
                "carrier": self.carrier_name
            }
            # 可以添加更多电信套餐...
        ]


class JSONDataSource(DataSource):
    """从JSON文件加载数据源"""
    
    def __init__(self, json_file: str, carrier_name: str):
        self.carrier_name = carrier_name
        self.json_file = json_file
        self._packages_data = self._load_from_json()
    
    def get_carrier_name(self) -> str:
        """获取运营商名称"""
        return self.carrier_name
    
    def get_packages(self) -> List[Dict]:
        """获取套餐数据"""
        return self._packages_data
    
    def _load_from_json(self) -> List[Dict]:
        """从JSON文件加载套餐数据"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as json_file_handle:
                data = json.load(json_file_handle)
                # 确保每个套餐都有carrier字段
                for package in data:
                    package['carrier'] = self.carrier_name
                return data
        except FileNotFoundError:
            print(f"警告：找不到数据文件 {self.json_file}")
            return []
        except json.JSONDecodeError as e:
            print(f"错误：JSON文件格式错误 {e}")
            return []


class DataSourceManager:
    """数据源管理器"""
    
    def __init__(self):
        self.data_sources: List[DataSource] = []
        self._register_default_sources()
    
    def _register_default_sources(self):
        """注册默认数据源"""
        self.register_source(ChinaMobileDataSource())
        # 可以根据需要启用其他运营商
        # self.register_source(ChinaUnicomDataSource())
        # self.register_source(ChinaTelecomDataSource())
    
    def register_source(self, source: DataSource):
        """注册数据源"""
        self.data_sources.append(source)
    
    def get_all_packages(self) -> List[Dict]:
        """获取所有数据源的套餐"""
        all_packages = []
        for source in self.data_sources:
            packages = source.get_packages()
            all_packages.extend(packages)
        return all_packages
    
    def get_packages_by_carrier(self, carrier_name: str) -> List[Dict]:
        """根据运营商获取套餐"""
        for source in self.data_sources:
            if source.get_carrier_name() == carrier_name:
                return source.get_packages()
        return []
    
    def get_available_carriers(self) -> List[str]:
        """获取可用的运营商列表"""
        return [source.get_carrier_name() for source in self.data_sources]
    
    def load_custom_data(self, json_file: str, carrier_name: str):
        """加载自定义数据源"""
        custom_source = JSONDataSource(json_file, carrier_name)
        self.register_source(custom_source)


# 数据验证工具
def validate_package_data(packages: List[Dict]) -> List[str]:
    """验证套餐数据格式"""
    errors = []
    required_fields = ['name', 'specs']
    required_specs = ['data', 'calls', 'price']
    
    for i, package in enumerate(packages):
        # 检查必需字段
        for field in required_fields:
            if field not in package:
                errors.append(f"套餐 {i}: 缺少字段 '{field}'")
        
        # 检查specs内容
        if 'specs' in package:
            specs = package['specs']
            for spec in required_specs:
                if spec not in specs:
                    errors.append(f"套餐 {i}: specs缺少字段 '{spec}'")
                elif not isinstance(specs[spec], (int, float)):
                    errors.append(f"套餐 {i}: specs.{spec} 应为数字类型")
    
    return errors


if __name__ == "__main__":
    # 示例用法
    manager = DataSourceManager()
    
    # 获取所有套餐
    all_packages = manager.get_all_packages()
    print(f"总共加载了 {len(all_packages)} 个套餐")
    
    # 获取运营商列表
    carriers = manager.get_available_carriers()
    print(f"支持的运营商: {carriers}")
    
    # 验证数据
    errors = validate_package_data(all_packages)
    if errors:
        print("数据验证错误:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("数据验证通过") 