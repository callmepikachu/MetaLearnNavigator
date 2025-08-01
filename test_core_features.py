#!/usr/bin/env python3
"""
核心功能测试脚本
测试MetaLearnNavigator的核心学习流程
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_core_workflow():
    """测试核心学习工作流程"""
    print("🎯 测试核心学习工作流程")
    print("=" * 50)
    
    # 1. 测试任务拆解
    print("\n📋 步骤1: 任务拆解")
    print("-" * 30)
    
    problem = "我想学习Python数据分析，包括pandas和matplotlib的使用"
    
    try:
        response = requests.post(f"{BASE_URL}/api/external/task-decomposition", 
                               json={"problem_statement": problem})
        if response.status_code == 200:
            decomposition = response.json()
            print(f"✅ 任务拆解成功")
            print(f"   生成节点数: {len(decomposition.get('nodes', []))}")
            print(f"   生成连线数: {len(decomposition.get('edges', []))}")
            
            # 显示生成的节点
            for i, node in enumerate(decomposition.get('nodes', [])[:3]):
                print(f"   节点{i+1}: {node.get('name', 'Unknown')}")
            
            return decomposition
        else:
            print(f"❌ 任务拆解失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 任务拆解异常: {e}")
        return None

def test_resource_search():
    """测试资源搜索功能"""
    print("\n📋 步骤2: 资源搜索")
    print("-" * 30)
    
    try:
        response = requests.post(f"{BASE_URL}/api/external/resource-search",
                               json={"query": "Python pandas tutorial", "task_context": "data analysis"})
        if response.status_code == 200:
            resources = response.json()
            print(f"✅ 资源搜索成功")
            print(f"   找到资源数: {len(resources.get('resources', []))}")
            
            # 显示前3个资源
            for i, resource in enumerate(resources.get('resources', [])[:3]):
                print(f"   资源{i+1}: {resource.get('title', 'Unknown')}")
            
            return resources
        else:
            print(f"❌ 资源搜索失败: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ 资源搜索异常: {e}")
        return None

def test_keyword_extraction():
    """测试关键词提取"""
    print("\n📋 步骤3: 关键词提取")
    print("-" * 30)
    
    # 导入关键词提取器进行本地测试
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        
        from services.keyword_extractor import KeywordExtractor
        
        extractor = KeywordExtractor()
        text = "我想学习Python数据分析，包括pandas库的使用、数据清洗、数据可视化和matplotlib绘图"
        
        keywords = extractor.extract_keywords(text, max_keywords=5)
        print(f"✅ 关键词提取成功")
        print(f"   提取的关键词: {', '.join(keywords)}")
        
        return keywords
    except Exception as e:
        print(f"❌ 关键词提取异常: {e}")
        return []

def test_subtask_generation():
    """测试子任务生成"""
    print("\n📋 步骤4: 子任务生成")
    print("-" * 30)
    
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        
        from services.subtask_generator import SubTaskGenerator
        
        generator = SubTaskGenerator()
        subtasks = generator.generate_subtasks(
            source_node_name="Python基础",
            target_node_name="数据分析",
            relationship_type="下级",
            problem_context="学习Python数据分析"
        )
        
        print(f"✅ 子任务生成成功")
        print(f"   生成子任务数: {len(subtasks)}")
        
        for i, task in enumerate(subtasks):
            print(f"   子任务{i+1}: {task.name}")
        
        return subtasks
    except Exception as e:
        print(f"❌ 子任务生成异常: {e}")
        return []

def test_flow_engine():
    """测试流程引擎"""
    print("\n📋 步骤5: 流程引擎")
    print("-" * 30)
    
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        
        from services.flow_engine import FlowEngine
        from models.schemas import JOLLevel, FOKLevel
        
        engine = FlowEngine()
        
        # 测试评分映射
        jol_score = engine.JOL_SCORES[JOLLevel.MOSTLY_REMEMBER]
        fok_score = engine.FOK_SCORES[FOKLevel.UNDERSTAND_WELL]
        
        print(f"✅ 流程引擎测试成功")
        print(f"   JOL评分示例: {jol_score}")
        print(f"   FOK评分示例: {fok_score}")
        
        return True
    except Exception as e:
        print(f"❌ 流程引擎测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🎯 MetaLearnNavigator 核心功能测试")
    print("=" * 60)
    
    # 等待服务启动
    print("⏳ 检查后端服务状态...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ 后端服务正常运行")
        else:
            print("❌ 后端服务异常")
            return
    except:
        print("❌ 无法连接到后端服务")
        return
    
    # 执行核心功能测试
    results = []
    
    # 测试各个核心功能
    results.append(("任务拆解", test_core_workflow() is not None))
    results.append(("资源搜索", test_resource_search() is not None))
    results.append(("关键词提取", test_keyword_extraction() != []))
    results.append(("子任务生成", test_subtask_generation() != []))
    results.append(("流程引擎", test_flow_engine()))
    
    # 统计结果
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print("\n" + "=" * 60)
    print("🎉 核心功能测试完成")
    print("=" * 60)
    print(f"总体结果: {passed}/{total} 个核心功能正常")
    
    for name, success in results:
        status = "✅" if success else "❌"
        print(f"{status} {name}")
    
    if passed == total:
        print("\n🎉 所有核心功能都正常工作！")
        print("📍 可以开始开发前端界面了")
    else:
        print(f"\n⚠️  有 {total - passed} 个功能需要修复")
    
    print("\n📋 下一步建议:")
    print("1. 访问 http://localhost:8000/docs 查看完整API文档")
    print("2. 开发前端用户界面")
    print("3. 集成完整的学习流程")

if __name__ == "__main__":
    main()
