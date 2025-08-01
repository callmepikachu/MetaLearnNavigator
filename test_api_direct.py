#!/usr/bin/env python3
"""
直接测试后端API
检查是否使用了OpenAI API
"""

import requests
import json
import os

def test_task_decomposition_api():
    """测试任务拆解API"""
    
    url = "http://localhost:8000/api/external/task-decomposition"
    
    test_cases = [
        "如何用内存管理大模型记忆",
        "学习React前端开发",
        "深度学习神经网络原理"
    ]
    
    for i, problem in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"测试用例 {i}: {problem}")
        print('='*60)
        
        try:
            # 发送POST请求
            response = requests.post(
                url,
                json={"problem_statement": problem},
                timeout=30
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"节点数量: {len(result.get('nodes', []))}")
                print(f"连线数量: {len(result.get('edges', []))}")
                
                print("\n生成的节点:")
                for j, node in enumerate(result.get('nodes', [])[:5]):
                    print(f"  {j+1}. {node.get('name', 'Unknown')}")
                    print(f"     描述: {node.get('description', 'No description')}")
                
                print("\n连线关系:")
                for j, edge in enumerate(result.get('edges', [])[:5]):
                    print(f"  {j+1}. {edge.get('source_id', 'Unknown')} -> {edge.get('target_id', 'Unknown')}")
                    print(f"     关系: {edge.get('relationship_type', 'Unknown')}")
                
                # 分析结果质量
                analyze_result_quality(result, problem)
                
            else:
                print(f"请求失败: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ 无法连接到后端服务")
            print("请确保后端服务在 http://localhost:8000 运行")
            break
        except requests.exceptions.Timeout:
            print("❌ 请求超时")
        except Exception as e:
            print(f"❌ 请求异常: {e}")

def analyze_result_quality(result, problem):
    """分析拆解结果质量"""
    print(f"\n📊 结果质量分析:")
    
    nodes = result.get('nodes', [])
    edges = result.get('edges', [])
    
    # 检查节点质量
    node_quality_score = 0
    
    # 1. 节点名称是否合理（不是单字符）
    single_char_nodes = [n for n in nodes if len(n.get('name', '')) <= 2]
    if len(single_char_nodes) == 0:
        node_quality_score += 2
        print("  ✅ 节点名称质量良好（无单字符节点）")
    else:
        print(f"  ❌ 发现 {len(single_char_nodes)} 个单字符节点")
    
    # 2. 节点描述是否详细
    detailed_descriptions = [n for n in nodes if len(n.get('description', '')) > 10]
    if len(detailed_descriptions) >= len(nodes) * 0.8:
        node_quality_score += 2
        print("  ✅ 节点描述详细")
    else:
        print("  ⚠️  节点描述可以更详细")
    
    # 3. 节点是否与问题相关
    problem_keywords = problem.lower().split()
    relevant_nodes = 0
    for node in nodes:
        node_name = node.get('name', '').lower()
        if any(keyword in node_name for keyword in problem_keywords if len(keyword) > 2):
            relevant_nodes += 1
    
    if relevant_nodes >= 2:
        node_quality_score += 2
        print(f"  ✅ 发现 {relevant_nodes} 个与问题相关的节点")
    else:
        print(f"  ⚠️  只有 {relevant_nodes} 个节点与问题明显相关")
    
    # 检查连线质量
    edge_quality_score = 0
    
    # 1. 连线数量是否合理
    if len(edges) >= len(nodes) - 1:  # 至少形成连通图
        edge_quality_score += 2
        print("  ✅ 连线数量合理")
    else:
        print("  ⚠️  连线数量可能不足")
    
    # 2. 关系类型是否多样化
    relationship_types = set(e.get('relationship_type', '') for e in edges)
    if len(relationship_types) >= 2:
        edge_quality_score += 2
        print(f"  ✅ 关系类型多样化: {list(relationship_types)}")
    else:
        print(f"  ⚠️  关系类型单一: {list(relationship_types)}")
    
    total_score = node_quality_score + edge_quality_score
    max_score = 8
    
    print(f"\n🎯 总体质量评分: {total_score}/{max_score} ({total_score/max_score*100:.1f}%)")
    
    if total_score >= 6:
        print("  🎉 拆解质量良好！")
        if total_score == max_score:
            print("  🚀 可能使用了AI API进行拆解")
        else:
            print("  🤖 使用了智能模拟拆解")
    else:
        print("  ⚠️  拆解质量需要改进")

def check_openai_config():
    """检查OpenAI配置"""
    print("🔍 检查OpenAI API配置:")
    
    # 检查环境变量
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print(f"  ✅ 环境变量中找到API密钥: {api_key[:10]}...")
    else:
        print("  ❌ 环境变量中未找到OPENAI_API_KEY")
    
    # 检查.env文件
    try:
        with open('backend/.env', 'r', encoding='utf-8') as f:
            env_content = f.read()
            if 'OPENAI_API_KEY' in env_content:
                print("  ✅ backend/.env文件中找到API密钥配置")
            else:
                print("  ❌ backend/.env文件中未找到API密钥配置")
    except FileNotFoundError:
        print("  ❌ 未找到backend/.env文件")
    except UnicodeDecodeError:
        print("  ⚠️  .env文件编码问题，跳过检查")

def main():
    """主函数"""
    print("🎯 MetaLearnNavigator API直接测试")
    print("=" * 60)
    
    # 检查OpenAI配置
    check_openai_config()
    
    # 测试任务拆解API
    test_task_decomposition_api()
    
    print(f"\n{'='*60}")
    print("📋 测试总结:")
    print("1. 如果节点名称是专业术语而不是单字符，说明使用了智能拆解")
    print("2. 如果质量评分很高，可能使用了OpenAI API")
    print("3. 如果质量评分中等，使用了智能模拟拆解")
    print("4. 如果质量评分很低，可能还在使用旧的简单拆解")
    print("=" * 60)

if __name__ == "__main__":
    main()
