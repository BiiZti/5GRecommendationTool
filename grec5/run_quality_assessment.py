#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合质量评估工具
整合代码质量检查、自动化测试、安全审计
符合评估标准中的代码质量和代码调试要求
"""

import os
import sys
import json
import time
from datetime import datetime
from .code_standards import CodeStandardsChecker


def run_comprehensive_assessment():
    """运行综合质量评估"""
    print("🏆 5G推荐工具 - 综合质量评估")
    print("=" * 60)
    print(f"📅 评估时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 项目文件列表
    project_files = [
        'recommendation_engine.py',
        'data_sources.py',
        'api_server.py',
        'gui.py',
        'config.json',
        'requirements.txt'
    ]
    
    assessment_results = {
        'timestamp': datetime.now().isoformat(),
        'code_quality': {},
        'code_debugging': {},
        'overall_score': 0
    }
    
    # 1. 代码质量评估 (10分)
    print("\n📝 1. 代码质量评估")
    print("-" * 40)
    
    try:
        checker = CodeStandardsChecker()
        quality_result = checker.check_project(project_files)
        
        print(f"✅ 检查完成: {quality_result['files_checked']} 个文件")
        print(f"📊 代码统计:")
        print(f"   📏 总行数: {quality_result['total_metrics']['lines']}")
        print(f"   🔧 函数数: {quality_result['total_metrics']['functions']}")
        print(f"   🏗️  类数: {quality_result['total_metrics']['classes']}")
        print(f"   📖 文档覆盖率: {quality_result['total_metrics']['docstring_coverage']}%")
        
        print(f"🚨 问题统计:")
        print(f"   ❌ 错误: {quality_result['total_issues']['error']}")
        print(f"   ⚠️  警告: {quality_result['total_issues']['warning']}")
        print(f"   ℹ️  信息: {quality_result['total_issues']['info']}")
        
        code_quality_score = quality_result['quality_score']['score']
        print(f"📝 代码质量评分: {code_quality_score}/10 ({quality_result['quality_score']['rating']})")
        
        assessment_results['code_quality'] = {
            'score': code_quality_score,
            'rating': quality_result['quality_score']['rating'],
            'details': quality_result
        }
        
    except Exception as e:
        print(f"❌ 代码质量检查失败: {e}")
        code_quality_score = 0
        assessment_results['code_quality'] = {'score': 0, 'error': str(e)}
    
    # 2. 代码调试能力评估 (10分)
    print(f"\n🐛 2. 代码调试能力评估")
    print("-" * 40)
    
    debug_score = assess_debugging_capabilities(project_files)
    assessment_results['code_debugging'] = debug_score
    
    print(f"🐛 代码调试评分: {debug_score['score']}/10 ({debug_score['rating']})")
    
    # 3. 综合评分计算
    overall_score = (code_quality_score + debug_score['score']) / 2
    assessment_results['overall_score'] = overall_score
    
    print(f"\n🎯 综合评估结果")
    print("=" * 40)
    print(f"📝 代码质量: {code_quality_score}/10")
    print(f"🐛 代码调试: {debug_score['score']}/10")
    print(f"🏆 综合得分: {overall_score:.1f}/10")
    
    # 评级
    if overall_score >= 9:
        overall_rating = "优秀 🌟"
    elif overall_score >= 8:
        overall_rating = "良好 👍"
    elif overall_score >= 6:
        overall_rating = "一般 ⭐"
    else:
        overall_rating = "需改进 ⚠️"
    
    print(f"📊 总体评级: {overall_rating}")
    
    # 4. 生成改进建议
    print(f"\n💡 改进建议")
    print("-" * 40)
    generate_improvement_suggestions(assessment_results)
    
    # 5. 保存评估报告
    save_assessment_report(assessment_results)
    
    return assessment_results


def assess_debugging_capabilities(project_files):
    """评估代码调试能力"""
    debug_features = {
        'error_handling': 0,      # 错误处理
        'logging': 0,             # 日志记录
        'type_hints': 0,          # 类型提示
        'documentation': 0,       # 文档完整性
        'test_coverage': 0,       # 测试覆盖
        'security_practices': 0   # 安全实践
    }
    
    total_files = 0
    
    for file_path in project_files:
        if not file_path.endswith('.py') or not os.path.exists(file_path):
            continue
            
        total_files += 1
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file_handle:
                content = file_handle.read()
            
            # 检查错误处理
            if 'try:' in content and 'except' in content:
                debug_features['error_handling'] += 1
            
            # 检查类型提示
            if 'from typing import' in content or 'import typing' in content:
                debug_features['type_hints'] += 1
            
            # 检查文档字符串
            if '"""' in content or "'''" in content:
                debug_features['documentation'] += 1
            
            # 检查日志记录
            if 'logging' in content or 'print(' in content:
                debug_features['logging'] += 1
            
            # 检查安全实践（简化版）
            if 'validate' in content.lower() or 'sanitize' in content.lower():
                debug_features['security_practices'] += 1
                
        except Exception as e:
            print(f"⚠️  无法分析文件 {file_path}: {e}")
    
    # 检查测试文件
    test_files = ['test_suite.py', 'test_*.py', '*_test.py']
    for pattern in test_files:
        if os.path.exists(pattern.replace('*', '')):
            debug_features['test_coverage'] = 1
            break
    
    # 计算调试能力评分
    total_possible = total_files * 5 + 1  # 5个特性 + 测试覆盖
    total_achieved = sum(debug_features.values())
    
    debug_score = min(10, (total_achieved / total_possible) * 10) if total_possible > 0 else 0
    
    # 评级
    if debug_score >= 8:
        rating = "优秀"
    elif debug_score >= 6:
        rating = "良好"
    elif debug_score >= 4:
        rating = "一般"
    else:
        rating = "需改进"
    
    print(f"   ✅ 错误处理: {debug_features['error_handling']}/{total_files} 文件")
    print(f"   🏷️  类型提示: {debug_features['type_hints']}/{total_files} 文件")
    print(f"   📖 文档字符串: {debug_features['documentation']}/{total_files} 文件")
    print(f"   📝 日志记录: {debug_features['logging']}/{total_files} 文件")
    print(f"   🔒 安全实践: {debug_features['security_practices']}/{total_files} 文件")
    print(f"   🧪 测试覆盖: {'✅' if debug_features['test_coverage'] else '❌'}")
    
    return {
        'score': round(debug_score, 1),
        'rating': rating,
        'features': debug_features,
        'details': {
            'total_files': total_files,
            'coverage_percentage': round((total_achieved / total_possible) * 100, 1) if total_possible > 0 else 0
        }
    }


def generate_improvement_suggestions(results):
    """生成改进建议"""
    suggestions = []
    
    # 基于代码质量结果的建议
    if 'code_quality' in results and 'details' in results['code_quality']:
        quality_details = results['code_quality']['details']
        
        if quality_details['total_issues']['error'] > 0:
            suggestions.append("🔧 修复代码错误，提高代码稳定性")
        
        if quality_details['total_issues']['warning'] > 5:
            suggestions.append("⚠️  减少代码警告，改善代码质量")
        
        if quality_details['total_metrics']['docstring_coverage'] < 70:
            suggestions.append("📖 增加文档字符串，提高代码可读性")
    
    # 基于调试能力结果的建议
    if 'code_debugging' in results:
        debug_details = results['code_debugging']
        
        if debug_details['features']['error_handling'] < debug_details['details']['total_files']:
            suggestions.append("🛡️  添加更多错误处理机制")
        
        if debug_details['features']['type_hints'] < debug_details['details']['total_files']:
            suggestions.append("🏷️  增加类型提示，提高代码安全性")
        
        if not debug_details['features']['test_coverage']:
            suggestions.append("🧪 添加单元测试，提高代码可靠性")
        
        if debug_details['features']['security_practices'] == 0:
            suggestions.append("🔒 加强安全验证和数据校验")
    
    # 通用建议
    if results['overall_score'] < 8:
        suggestions.append("📚 参考最佳实践，持续改进代码质量")
        suggestions.append("🔍 建立代码审查流程")
    
    if not suggestions:
        suggestions.append("🎉 代码质量良好，继续保持!")
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"{i}. {suggestion}")


def save_assessment_report(results):
    """保存评估报告"""
    report_file = f"quality_assessment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as report_file_handle:
            json.dump(results, report_file_handle, ensure_ascii=False, indent=2)
        print(f"\n📄 评估报告已保存: {report_file}")
    except Exception as e:
        print(f"⚠️  保存报告失败: {e}")


def check_project_structure():
    """检查项目结构完整性"""
    print("\n🏗️  项目结构检查")
    print("-" * 40)
    
    required_files = {
        'recommendation_engine.py': '推荐引擎核心',
        'data_sources.py': '数据源管理',
        'api_server.py': 'API服务器',
        'gui.py': '图形界面',
        'config.json': '配置文件',
        'requirements.txt': '依赖列表',
        'README.md': '项目文档'
    }
    
    structure_score = 0
    total_files = len(required_files)
    
    for file_path, description in required_files.items():
        if os.path.exists(file_path):
            print(f"✅ {file_path} - {description}")
            structure_score += 1
        else:
            print(f"❌ {file_path} - {description} (缺失)")
    
    print(f"\n📊 结构完整性: {structure_score}/{total_files} ({structure_score/total_files*100:.1f}%)")
    return structure_score / total_files


def main():
    """主函数"""
    try:
        # 检查项目结构
        structure_score = check_project_structure()
        
        # 运行综合评估
        results = run_comprehensive_assessment()
        
        print(f"\n🎯 最终评估总结")
        print("=" * 60)
        print(f"🏗️  项目结构: {structure_score*10:.1f}/10")
        print(f"📝 代码质量: {results['code_quality'].get('score', 0)}/10")
        print(f"🐛 代码调试: {results['code_debugging']['score']}/10")
        print(f"🏆 综合评分: {results['overall_score']:.1f}/10")
        
        # 符合评估标准判断
        code_quality_level = ""
        if results['code_quality'].get('score', 0) >= 8:
            code_quality_level = "代码规范，易读、易维护、可扩展 (8-10分)"
        elif results['code_quality'].get('score', 0) >= 4:
            code_quality_level = "代码质量一般，部分满足管理要求 (4-7分)"
        else:
            code_quality_level = "代码质量差，不符合管理要求 (0-3分)"
        
        debug_level = ""
        if results['code_debugging']['score'] >= 8:
            debug_level = "调试管理完善，无严重漏洞 (8-10分)"
        elif results['code_debugging']['score'] >= 4:
            debug_level = "调试管理一般，存在部分可接受的漏洞 (4-7分)"
        else:
            debug_level = "调试管理差，存在严重漏洞 (0-3分)"
        
        print(f"\n📋 评估标准对照:")
        print(f"📝 代码质量: {code_quality_level}")
        print(f"🐛 代码调试: {debug_level}")
        
        return results
        
    except Exception as e:
        print(f"❌ 评估过程出错: {e}")
        return None


if __name__ == '__main__':
    main() 