#!/usr/bin/env python3
"""
测试OpenAI API密钥是否有效
"""

import os
import requests
from dotenv import load_dotenv

def test_openai_key():
    """测试OpenAI API密钥"""
    
    # 加载.env文件
    load_dotenv('backend/.env')
    
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ 未找到API密钥")
        return False
    
    print(f"🔑 找到API密钥: {api_key[:10]}...{api_key[-10:]}")
    
    # 测试API调用
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Hello, this is a test."}],
                "max_tokens": 10
            },
            timeout=10
        )
        
        print(f"📡 API响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ OpenAI API密钥有效！")
            result = response.json()
            print(f"📝 测试响应: {result['choices'][0]['message']['content']}")
            return True
        else:
            print(f"❌ API调用失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API调用异常: {e}")
        return False

if __name__ == "__main__":
    print("🧪 测试OpenAI API密钥有效性")
    print("=" * 40)
    
    if test_openai_key():
        print("\n🎉 API密钥有效，后端应该能使用OpenAI API进行拆解")
        print("💡 如果后端没有使用OpenAI API，可能需要重启后端服务")
    else:
        print("\n⚠️  API密钥无效或网络问题，系统会使用智能模拟拆解")
