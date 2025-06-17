#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5G套餐自动推荐工具 - GUI桌面版
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Optional, Dict, List, Any

# 导入新的模块化组件
from recommendation_engine import RecommendationEngine
from data_sources import DataSourceManager

class RecommendationApp:
    """主应用程序类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("📱 通用套餐自动推荐工具")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f8ff')
        
        # 初始化核心组件
        self.engine = RecommendationEngine()
        self.data_manager = DataSourceManager()
        
        # 设置主题样式
        self.setup_styles()
        
        # 创建主界面
        self.create_widgets()
        
        # 居中窗口
        self.center_window()
    
    def setup_styles(self):
        """设置主题样式"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # 配置样式
        self.style.configure('Title.TLabel', 
                           font=('Microsoft YaHei', 18, 'bold'),
                           background='#f0f8ff',
                           foreground='#2c3e50')
        
        self.style.configure('Heading.TLabel',
                           font=('Microsoft YaHei', 12, 'bold'),
                           background='#f0f8ff',
                           foreground='#34495e')
        
        self.style.configure('Info.TLabel',
                           font=('Microsoft YaHei', 9),
                           background='#f0f8ff',
                           foreground='#7f8c8d')
        
        self.style.configure('Recommend.TButton',
                           font=('Microsoft YaHei', 12, 'bold'))
    
    def center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        pos_x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    def create_widgets(self):
        """创建界面组件"""
        # 主容器
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="📱 通用套餐自动推荐工具", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # 创建水平容器
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧输入区域
        self.create_input_panel(content_frame)
        
        # 右侧结果区域
        self.create_result_panel(content_frame)
    
    def create_input_panel(self, parent):
        """创建输入面板"""
        input_frame = ttk.LabelFrame(parent, text="📝 请输入您的需求", padding="15")
        input_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # 流量输入
        ttk.Label(input_frame, text="每月流量需求 (GB):", style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.data_var = tk.StringVar(value="30")
        self.data_entry = ttk.Entry(input_frame, textvariable=self.data_var, font=('Microsoft YaHei', 10), width=20)
        self.data_entry.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(input_frame, text="建议范围: 1-500GB", style='Info.TLabel').pack(anchor=tk.W, pady=(0, 15))
        
        # 通话输入
        ttk.Label(input_frame, text="每月通话时长 (分钟):", style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.calls_var = tk.StringVar(value="500")
        self.calls_entry = ttk.Entry(input_frame, textvariable=self.calls_var, font=('Microsoft YaHei', 10), width=20)
        self.calls_entry.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(input_frame, text="建议范围: 0-10000分钟", style='Info.TLabel').pack(anchor=tk.W, pady=(0, 15))
        
        # 预算输入
        ttk.Label(input_frame, text="预算范围 (元/月):", style='Heading.TLabel').pack(anchor=tk.W, pady=(0, 5))
        self.budget_var = tk.StringVar(value="150")
        self.budget_entry = ttk.Entry(input_frame, textvariable=self.budget_var, font=('Microsoft YaHei', 10), width=20)
        self.budget_entry.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(input_frame, text="建议范围: 50-1000元", style='Info.TLabel').pack(anchor=tk.W, pady=(0, 20))
        
        # 按钮区域
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 推荐按钮
        recommend_btn = ttk.Button(button_frame, text="🚀 开始推荐", 
                                 command=self.get_recommendations, style='Recommend.TButton')
        recommend_btn.pack(fill=tk.X, pady=(0, 10))
        

        
        # 使用说明
        ttk.Separator(input_frame, orient='horizontal').pack(fill=tk.X, pady=(20, 10))
        help_text = """💡 使用说明：
        
• 根据实际使用情况填写需求
• 系统会自动匹配最优套餐
• 支持26种中国移动套餐对比"""
        
        help_label = tk.Label(input_frame, text=help_text, 
                             font=('Microsoft YaHei', 9), 
                             bg='#f0f8ff', fg='#7f8c8d', 
                             justify=tk.LEFT, wraplength=250)
        help_label.pack(anchor=tk.W, pady=(0, 10))
    
    def create_result_panel(self, parent):
        """创建结果面板"""
        result_frame = ttk.LabelFrame(parent, text="🌟 推荐结果", padding="15")
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 直接创建推荐结果显示区域
        self.create_result_display(result_frame)
    
    def create_result_display(self, parent):
        """创建推荐结果显示区域"""
        # 滚动文本框显示推荐结果
        self.result_text = scrolledtext.ScrolledText(
            parent, 
            wrap=tk.WORD, 
            font=('Microsoft YaHei', 10),
            height=25
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 初始显示提示信息
        welcome_text = """欢迎使用中国移动5G套餐自动推荐工具！🎉

📱 基于中国移动官方真实套餐数据
🔗 数据来源: http://www.y576.com/aricle.asp?id=48

请在左侧输入您的需求：
• 每月流量需求 (GB)
• 每月通话时长 (分钟) 
• 预算范围 (元/月)

然后点击"开始推荐"按钮，系统将为您分析并推荐最适合的移动5G套餐。

💡 推荐系统特点：
✓ 多维度匹配分析
✓ 性价比自动评估  
✓ 避免资源浪费
✓ 基于真实套餐数据

📋 可选套餐范围：
• 8元-319元全价位覆盖
• 0.1GB-100GB流量配置
• 4G/5G网络全覆盖
• 互联网卡、标准套餐、融合套餐多选择

🎯 让我们开始为您找到最优的移动5G套餐吧！"""
        
        self.result_text.insert(tk.END, welcome_text)
        self.result_text.config(state=tk.DISABLED)
    

    
    def validate_input(self):
        """验证用户输入"""
        try:
            data = float(self.data_var.get())
            calls = float(self.calls_var.get())
            budget = float(self.budget_var.get())
            
            if not (1 <= data <= 500):
                raise ValueError("流量需求应在1-500GB之间")
            if not (0 <= calls <= 10000):
                raise ValueError("通话时长应在0-10000分钟之间")
            if not (50 <= budget <= 1000):
                raise ValueError("预算应在50-1000元之间")
            
            return data, calls, budget
        except ValueError as e:
            messagebox.showerror("输入错误", f"请检查输入数据：\n{str(e)}")
            return None
    
    def get_recommendations(self):
        """获取推荐结果"""
        # 验证输入
        validation_result = self.validate_input()
        if validation_result is None:
            return
        
        data, calls, budget = validation_result
        
        # 构建用户需求
        user_needs = {"data": data, "calls": calls}
        
        # 获取套餐数据
        packages = self.data_manager.get_all_packages()
        
        # 获取推荐
        recommendations = self.engine.recommend(user_needs, budget, packages)
        
        # 显示结果
        self.display_recommendations(recommendations, data, calls, budget)
    
    def display_recommendations(self, recommendations: List[Dict], data: float, calls: float, budget: float) -> None:
        """显示推荐结果"""
        # 启用文本框编辑
        self.result_text.config(state=tk.NORMAL)
        # 清空之前的结果
        self.result_text.delete(1.0, tk.END)
        
        # 显示用户输入摘要
        self._display_user_summary(data, calls, budget)
        
        if not recommendations:
            self._display_no_recommendations(data, calls, budget)
            return
        
        self._display_recommendation_results(recommendations)
        
        # 禁用文本框编辑
        self.result_text.config(state=tk.DISABLED)
    
    def _display_user_summary(self, data: float, calls: float, budget: float) -> None:
        """显示用户需求摘要"""
        self.result_text.insert(tk.END, "📋 您的需求摘要\n")
        self.result_text.insert(tk.END, "=" * 60 + "\n")
        self.result_text.insert(tk.END, f"💾 月流量需求: {data}GB\n")
        self.result_text.insert(tk.END, f"📞 月通话时长: {calls}分钟\n")
        self.result_text.insert(tk.END, f"💰 预算范围: {budget}元/月\n\n")
    
    def _display_no_recommendations(self, data: float, calls: float, budget: float) -> None:
        """显示无推荐结果的分析"""
        self.result_text.insert(tk.END, "😔 抱歉，没有找到完全符合您需求的套餐\n\n")
        
        # 使用推荐引擎的分析功能
        user_needs = {"data": data, "calls": calls}
        packages = self.data_manager.get_all_packages()
        analysis = self.engine.analyze_no_match_reason(user_needs, budget, packages)
        
        # 显示分析结果
        self.result_text.insert(tk.END, "📊 原因分析：\n")
        
        if analysis["over_budget_products"]:
            min_price = min(product.get("specs", {}).get("price", product.get("price", 0)) 
                          for product in analysis["over_budget_products"])
            self.result_text.insert(tk.END, f"• 有满足需求的套餐，但最低需要{min_price}元/月\n")
        
        for need_key, products_list in analysis["insufficient_specs"].items():
            if products_list:
                max_spec = max(product.get("specs", {}).get(need_key, 0) for product in products_list)
                need_name = "流量" if need_key == "data" else "通话时长"
                unit = "GB" if need_key == "data" else "分钟"
                self.result_text.insert(tk.END, f"• 预算内最大{need_name}只有{max_spec}{unit}\n")
        
        # 显示建议
        if analysis["suggestions"]:
            self.result_text.insert(tk.END, "\n💡 建议：\n")
            for suggestion in analysis["suggestions"]:
                self.result_text.insert(tk.END, f"• {suggestion}\n")
        
        # 通用建议
        self.result_text.insert(tk.END, "• 考虑使用WiFi减少流量消耗\n")
        self.result_text.insert(tk.END, "• 查看是否有其他运营商套餐选择\n")
        
        self.result_text.config(state=tk.DISABLED)
    
    def _display_recommendation_results(self, recommendations: List[Dict]) -> None:
        """显示推荐结果详情"""
        self.result_text.insert(tk.END, f"🎯 为您找到 {len(recommendations)} 个推荐套餐\n")
        self.result_text.insert(tk.END, "=" * 60 + "\n\n")
        
        for index, recommendation in enumerate(recommendations, 1):
            self._display_single_recommendation(recommendation, index)
    
    def _display_single_recommendation(self, recommendation: Dict, index: int) -> None:
        """显示单个推荐结果"""
        package = recommendation["product"]
        score = recommendation["score"]
        reason = recommendation["match_reason"]
        usage_score = recommendation.get("usage_score", 0)
        price_score = recommendation.get("price_score", 0)
        
        # 获取套餐规格
        specs = package.get("specs", {})
        carrier = package.get("carrier", "未知运营商")
        
        # 标识最佳推荐
        if index == 1:
            self.result_text.insert(tk.END, f"🌟 【最佳推荐】 推荐 #{index}\n")
        else:
            self.result_text.insert(tk.END, f"📱 推荐 #{index}\n")
        
        self.result_text.insert(tk.END, f"📡 运营商: {carrier}\n")
        self.result_text.insert(tk.END, f"📦 套餐名称: {package['name']}\n")
        self.result_text.insert(tk.END, f"📋 套餐类型: {package.get('type', '标准套餐')}\n")
        self.result_text.insert(tk.END, f"💵 月费: ¥{specs.get('price', 0)}\n")
        self.result_text.insert(tk.END, f"📊 流量: {specs.get('data', 0)}GB | 通话: {specs.get('calls', 0)}分钟\n")
        self.result_text.insert(tk.END, f"⭐ 综合评分: {score:.2f} (功能匹配: {usage_score:.2f} | 价格优势: {price_score:.2f})\n")
        
        # 显示特色功能
        features = package.get('features', [])
        if features:
            features_str = "、".join(features)
            self.result_text.insert(tk.END, f"🎁 特色功能: {features_str}\n")
        
        # 显示推荐理由
        self.result_text.insert(tk.END, f"💡 推荐理由: {reason}\n")
        
        # 性价比分析
        self._display_value_analysis(specs)
        
        self.result_text.insert(tk.END, "-" * 50 + "\n\n")
    
    def _display_value_analysis(self, specs: Dict) -> None:
        """显示性价比分析"""
        package_price = specs.get('price', 1)
        package_data = specs.get('data', 0)
        
        if package_price > 0:
            value_ratio = package_data / package_price
            if value_ratio > 0.4:
                value_desc = "高性价比 💎"
            elif value_ratio > 0.25:
                value_desc = "性价比良好 👍"
            else:
                value_desc = "标准价格 ⭐"
        else:
            value_desc = "价格异常 ❓"
        
        self.result_text.insert(tk.END, f"📈 性价比: {value_desc}\n")
    


def main():
    """主函数"""
    try:
        # 创建主窗口
        root = tk.Tk()
        
        # 创建应用
        app = RecommendationApp(root)
        
        # 运行应用
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("错误", f"应用启动失败：{str(e)}")

if __name__ == "__main__":
    main() 