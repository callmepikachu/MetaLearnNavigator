#!/usr/bin/env python3
"""
后端API测试脚本
用于验证后端服务是否正常工作
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"

def test_health_check():
    """测试健康检查接口"""
    print("🔍 测试健康检查接口...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 健康检查通过")
            return True
        else:
            print(f"❌ 健康检查失败: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务，请确保后端服务已启动")
        return False
    except Exception as e:
        print(f"❌ 健康检查异常: {e}")
        return False

def test_create_session():
    """测试创建学习会话"""
    print("🔍 测试创建学习会话...")
    try:
        data = {
            "problem_statement": "我想学习Python编程基础"
        }
        response = requests.post(f"{BASE_URL}/api/learning-flow/sessions", json=data)
        if response.status_code == 200:
            session_data = response.json()
            print(f"✅ 学习会话创建成功: {session_data['id']}")
            return session_data
        else:
            print(f"❌ 创建会话失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 创建会话异常: {e}")
        return None

def test_task_decomposition():
    """测试任务拆解"""
    print("🔍 测试任务拆解...")
    try:
        data = {
            "problem_statement": "我想学习Python编程基础"
        }
        response = requests.post(f"{BASE_URL}/api/external/task-decomposition", json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 任务拆解成功: 生成了 {len(result.get('nodes', []))} 个节点")
            return result
        else:
            print(f"❌ 任务拆解失败: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ 任务拆解异常: {e}")
        return None

def test_knowledge_cards():
    """测试知识卡片功能"""
    print("🔍 测试知识卡片功能...")
    try:
        # 创建知识卡片
        data = {
            "title": "Python基础语法",
            "content": "Python是一种高级编程语言，语法简洁易读。",
            "keywords": ["Python", "编程", "语法"]
        }
        response = requests.post(f"{BASE_URL}/api/knowledge-cards/", json=data)
        if response.status_code == 200:
            card = response.json()
            print(f"✅ 知识卡片创建成功: {card['id']}")
            
            # 测试搜索
            search_response = requests.get(f"{BASE_URL}/api/knowledge-cards/search/?query=Python")
            if search_response.status_code == 200:
                results = search_response.json()
                print(f"✅ 知识卡片搜索成功: 找到 {len(results)} 个结果")
                return True
            else:
                print(f"❌ 知识卡片搜索失败: {search_response.status_code}")
                return False
        else:
            print(f"❌ 知识卡片创建失败: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ 知识卡片测试异常: {e}")
        return False

def test_api_docs():
    """测试API文档是否可访问"""
    print("🔍 测试API文档...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            print("✅ API文档可访问")
            return True
        else:
            print(f"❌ API文档访问失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API文档测试异常: {e}")
        return False

def main():
    """主测试函数"""
    print("🎯 MetaLearnNavigator 后端API测试")
    print("=" * 50)
    
    # 等待服务启动
    print("⏳ 等待后端服务启动...")
    time.sleep(2)
    
    tests = [
        ("健康检查", test_health_check),
        ("API文档", test_api_docs),
        ("创建学习会话", test_create_session),
        ("任务拆解", test_task_decomposition),
        ("知识卡片", test_knowledge_cards),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
        time.sleep(1)  # 避免请求过快
    
    print("\n" + "=" * 50)
    print(f"🎉 测试完成: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("✅ 所有测试通过！后端服务运行正常")
        print(f"📍 API文档: {BASE_URL}/docs")
        print(f"📍 健康检查: {BASE_URL}/health")
    else:
        print("❌ 部分测试失败，请检查后端服务")
        sys.exit(1)

if __name__ == "__main__":
    main()
