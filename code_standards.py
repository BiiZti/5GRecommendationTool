#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
代码标准检查工具
检查代码规范性、可读性、可维护性、可扩展性
"""

import ast
import os
import re
from typing import List, Dict, Tuple
import json


class CodeStandardsChecker:
    """代码标准检查器"""
    
    def __init__(self):
        self.issues = []
        self.metrics = {
            'readability': 0,
            'maintainability': 0,
            'scalability': 0,
            'total_lines': 0,
            'total_functions': 0,
            'total_classes': 0,
            'docstring_coverage': 0
        }
    
    def check_file(self, file_path: str) -> Dict:
        """检查单个文件"""
        if not os.path.exists(file_path):
            return {'error': f'文件不存在: {file_path}'}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file_handle:
                content = file_handle.read()
            
            tree = ast.parse(content)
            file_issues = []
            
            # 检查各项标准
            file_issues.extend(self._check_docstrings(tree, file_path))
            file_issues.extend(self._check_function_complexity(tree, file_path))
            file_issues.extend(self._check_naming_conventions(tree, file_path))
            file_issues.extend(self._check_imports(tree, file_path))
            file_issues.extend(self._check_type_hints(content, file_path))
            file_issues.extend(self._check_code_structure(tree, file_path))
            
            # 计算指标
            metrics = self._calculate_file_metrics(tree, content)
            
            return {
                'file': file_path,
                'issues': file_issues,
                'metrics': metrics
            }
            
        except Exception as e:
            return {'error': f'解析文件失败 {file_path}: {e}'}
    
    def _check_docstrings(self, tree: ast.AST, file_path: str) -> List[Dict]:
        """检查文档字符串"""
        issues = []
        
        class DocstringVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                if not ast.get_docstring(node):
                    if not node.name.startswith('_'):  # 忽略私有方法
                        issues.append({
                            'type': '缺少文档字符串',
                            'level': 'warning',
                            'line': node.lineno,
                            'message': f'函数 {node.name} 缺少文档字符串'
                        })
                self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                if not ast.get_docstring(node):
                    issues.append({
                        'type': '缺少文档字符串',
                        'level': 'warning', 
                        'line': node.lineno,
                        'message': f'类 {node.name} 缺少文档字符串'
                    })
                self.generic_visit(node)
        
        visitor = DocstringVisitor()
        visitor.visit(tree)
        return issues
    
    def _check_function_complexity(self, tree: ast.AST, file_path: str) -> List[Dict]:
        """检查函数复杂度"""
        issues = []
        
        class ComplexityVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                # 简单的行数复杂度检查
                func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                
                if func_lines > 50:
                    issues.append({
                        'type': '函数过长',
                        'level': 'error',
                        'line': node.lineno,
                        'message': f'函数 {node.name} 有 {func_lines} 行，建议拆分'
                    })
                elif func_lines > 30:
                    issues.append({
                        'type': '函数较长',
                        'level': 'warning',
                        'line': node.lineno,
                        'message': f'函数 {node.name} 有 {func_lines} 行，考虑优化'
                    })
                
                # 检查参数数量
                arg_count = len(node.args.args)
                if arg_count > 6:
                    issues.append({
                        'type': '参数过多',
                        'level': 'warning',
                        'line': node.lineno,
                        'message': f'函数 {node.name} 有 {arg_count} 个参数，建议减少'
                    })
                
                self.generic_visit(node)
        
        visitor = ComplexityVisitor()
        visitor.visit(tree)
        return issues
    
    def _check_naming_conventions(self, tree: ast.AST, file_path: str) -> List[Dict]:
        """检查命名约定"""
        issues = []
        
        class NamingVisitor(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                # 检查函数命名（snake_case）
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    issues.append({
                        'type': '命名规范',
                        'level': 'warning',
                        'line': node.lineno,
                        'message': f'函数名 {node.name} 不符合snake_case规范'
                    })
                self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                # 检查类命名（PascalCase）
                if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                    issues.append({
                        'type': '命名规范',
                        'level': 'warning',
                        'line': node.lineno,
                        'message': f'类名 {node.name} 不符合PascalCase规范'
                    })
                self.generic_visit(node)
            
            def visit_Name(self, node):
                # 检查变量命名
                if isinstance(node.ctx, ast.Store):
                    name = node.id
                    if len(name) == 1 and name not in ['i', 'j', 'k', 'x', 'y', 'z']:
                        issues.append({
                            'type': '变量命名',
                            'level': 'info',
                            'line': node.lineno,
                            'message': f'变量名 {name} 过短，建议使用更有意义的名称'
                        })
                self.generic_visit(node)
        
        visitor = NamingVisitor()
        visitor.visit(tree)
        return issues
    
    def _check_imports(self, tree: ast.AST, file_path: str) -> List[Dict]:
        """检查导入语句"""
        issues = []
        imports = []
        
        class ImportVisitor(ast.NodeVisitor):
            def visit_Import(self, node):
                for alias in node.names:
                    imports.append(alias.name)
            
            def visit_ImportFrom(self, node):
                if node.module:
                    for alias in node.names:
                        imports.append(f"{node.module}.{alias.name}")
        
        visitor = ImportVisitor()
        visitor.visit(tree)
        
        # 检查未使用的导入（简化版本）
        # 这里可以扩展更复杂的分析
        
        return issues
    
    def _check_type_hints(self, content: str, file_path: str) -> List[Dict]:
        """检查类型提示"""
        issues = []
        
        # 检查是否使用了typing模块
        if 'from typing import' in content or 'import typing' in content:
            # 文件使用了类型提示，这是好的实践
            pass
        else:
            lines = content.split('\n')
            func_lines = [i for i, line in enumerate(lines) if 'def ' in line and not line.strip().startswith('#')]
            
            if len(func_lines) > 3:  # 如果有超过3个函数但没有类型提示
                issues.append({
                    'type': '类型提示',
                    'level': 'info',
                    'line': 1,
                    'message': '建议添加类型提示以提高代码可读性'
                })
        
        return issues
    
    def _check_code_structure(self, tree: ast.AST, file_path: str) -> List[Dict]:
        """检查代码结构"""
        issues = []
        
        class StructureVisitor(ast.NodeVisitor):
            def __init__(self):
                self.class_count = 0
                self.function_count = 0
                self.max_nesting = 0
                self.current_nesting = 0
            
            def visit_ClassDef(self, node):
                self.class_count += 1
                self.generic_visit(node)
            
            def visit_FunctionDef(self, node):
                self.function_count += 1
                self.generic_visit(node)
            
            def visit_If(self, node):
                self.current_nesting += 1
                self.max_nesting = max(self.max_nesting, self.current_nesting)
                self.generic_visit(node)
                self.current_nesting -= 1
            
            def visit_For(self, node):
                self.current_nesting += 1
                self.max_nesting = max(self.max_nesting, self.current_nesting)
                self.generic_visit(node)
                self.current_nesting -= 1
            
            def visit_While(self, node):
                self.current_nesting += 1
                self.max_nesting = max(self.max_nesting, self.current_nesting)
                self.generic_visit(node)
                self.current_nesting -= 1
        
        visitor = StructureVisitor()
        visitor.visit(tree)
        
        # 检查嵌套深度
        if visitor.max_nesting > 4:
            issues.append({
                'type': '代码嵌套',
                'level': 'warning',
                'line': 1,
                'message': f'最大嵌套深度 {visitor.max_nesting}，建议重构'
            })
        
        return issues
    
    def _calculate_file_metrics(self, tree: ast.AST, content: str) -> Dict:
        """计算文件指标"""
        lines = content.split('\n')
        total_lines = len([line for line in lines if line.strip()])
        
        class MetricsVisitor(ast.NodeVisitor):
            def __init__(self):
                self.functions = []
                self.classes = []
                self.docstring_count = 0
                self.total_items = 0
            
            def visit_FunctionDef(self, node):
                self.functions.append(node.name)
                self.total_items += 1
                if ast.get_docstring(node):
                    self.docstring_count += 1
                self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                self.classes.append(node.name)
                self.total_items += 1
                if ast.get_docstring(node):
                    self.docstring_count += 1
                self.generic_visit(node)
        
        visitor = MetricsVisitor()
        visitor.visit(tree)
        
        docstring_coverage = (visitor.docstring_count / visitor.total_items * 100) if visitor.total_items > 0 else 0
        
        return {
            'lines': total_lines,
            'functions': len(visitor.functions),
            'classes': len(visitor.classes),
            'docstring_coverage': round(docstring_coverage, 1)
        }
    
    def check_project(self, project_files: List[str]) -> Dict:
        """检查整个项目"""
        all_results = []
        total_issues = {'error': 0, 'warning': 0, 'info': 0}
        total_metrics = {
            'lines': 0,
            'functions': 0,
            'classes': 0,
            'docstring_coverage': []
        }
        
        for file_path in project_files:
            if file_path.endswith('.py'):
                result = self.check_file(file_path)
                if 'error' not in result:
                    all_results.append(result)
                    
                    # 统计问题
                    for issue in result['issues']:
                        total_issues[issue['level']] += 1
                    
                    # 累计指标
                    metrics = result['metrics']
                    total_metrics['lines'] += metrics['lines']
                    total_metrics['functions'] += metrics['functions']
                    total_metrics['classes'] += metrics['classes']
                    if metrics['docstring_coverage'] > 0:
                        total_metrics['docstring_coverage'].append(metrics['docstring_coverage'])
        
        # 计算平均文档覆盖率
        avg_docstring_coverage = (
            sum(total_metrics['docstring_coverage']) / len(total_metrics['docstring_coverage'])
            if total_metrics['docstring_coverage'] else 0
        )
        
        # 计算质量评分
        quality_score = self._calculate_quality_score(total_issues, avg_docstring_coverage)
        
        return {
            'files_checked': len(all_results),
            'total_issues': total_issues,
            'total_metrics': {
                'lines': total_metrics['lines'],
                'functions': total_metrics['functions'],
                'classes': total_metrics['classes'],
                'docstring_coverage': round(avg_docstring_coverage, 1)
            },
            'quality_score': quality_score,
            'details': all_results
        }
    
    def _calculate_quality_score(self, issues: Dict, docstring_coverage: float) -> Dict:
        """计算质量评分"""
        # 基础分数
        base_score = 10.0
        
        # 错误扣分
        base_score -= issues['error'] * 0.5
        # 警告扣分
        base_score -= issues['warning'] * 0.2
        # 信息扣分
        base_score -= issues['info'] * 0.1
        
        # 文档覆盖率加分
        if docstring_coverage >= 80:
            base_score += 0.5
        elif docstring_coverage >= 60:
            base_score += 0.2
        
        # 确保分数在0-10之间
        final_score = max(0, min(10, base_score))
        
        # 评级
        if final_score >= 9:
            rating = "优秀"
        elif final_score >= 8:
            rating = "良好"
        elif final_score >= 6:
            rating = "一般"
        else:
            rating = "需改进"
        
        return {
            'score': round(final_score, 1),
            'rating': rating
        }


def main():
    """主函数"""
    print("🔍 代码标准检查工具")
    print("=" * 50)
    
    # 检查项目文件
    project_files = [
        'recommendation_engine.py',
        'data_sources.py',
        'api_server.py', 
        'gui.py'
    ]
    
    checker = CodeStandardsChecker()
    result = checker.check_project(project_files)
    
    print(f"📁 检查文件数: {result['files_checked']}")
    print(f"📏 总代码行数: {result['total_metrics']['lines']}")
    print(f"🔧 总函数数: {result['total_metrics']['functions']}")
    print(f"🏗️  总类数: {result['total_metrics']['classes']}")
    print(f"📖 文档覆盖率: {result['total_metrics']['docstring_coverage']}%")
    
    print(f"\n🚨 问题统计:")
    print(f"❌ 错误: {result['total_issues']['error']}")
    print(f"⚠️  警告: {result['total_issues']['warning']}")
    print(f"ℹ️  信息: {result['total_issues']['info']}")
    
    print(f"\n⭐ 质量评分: {result['quality_score']['score']}/10 ({result['quality_score']['rating']})")
    
    # 详细报告
    if any(result['total_issues'].values()):
        print(f"\n📋 详细问题列表:")
        for file_result in result['details']:
            if file_result['issues']:
                print(f"\n📄 {file_result['file']}:")
                for issue in file_result['issues']:
                    level_icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}[issue['level']]
                    print(f"  {level_icon} 第{issue['line']}行: {issue['message']}")
    
    return result


if __name__ == '__main__':
    main() 