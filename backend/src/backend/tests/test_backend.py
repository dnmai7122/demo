#!/usr/bin/env python3
"""
Quick test script for FastAPI backend - Sign Language Learning API
"""

import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check: PASS")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check: FAIL (status {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is it running?")
        print("   Start it with: python run_backend.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_get_all_topics():
    """Test get all topics"""
    print("\n📚 Testing get all topics...")
    try:
        response = requests.get(f"{BASE_URL}/api/topics")
        if response.status_code == 200:
            data = response.json()
            print("✅ Get all topics: PASS")
            print(f"   Found {len(data.get('data', []))} topics")
            if data.get('data'):
                print(f"   First topic: {data['data'][0].get('name')}")
            return True
        else:
            print(f"❌ Get all topics: FAIL (status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_get_all_lessons():
    """Test get all lessons"""
    print("\n📝 Testing get all lessons...")
    try:
        response = requests.get(f"{BASE_URL}/api/lessons")
        if response.status_code == 200:
            data = response.json()
            print("✅ Get all lessons: PASS")
            print(f"   Found {len(data.get('data', []))} lessons")
            return True
        else:
            print(f"❌ Get all lessons: FAIL (status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_get_lessons_by_topic():
    """Test get lessons by topic"""
    print("\n🎯 Testing get lessons by topic (topic_id=12)...")
    try:
        response = requests.get(f"{BASE_URL}/api/topics/12/lessons")
        if response.status_code == 200:
            data = response.json()
            print("✅ Get lessons by topic: PASS")
            print(f"   Found {len(data.get('data', []))} lessons for topic 12")
            return True
        else:
            print(f"❌ Get lessons by topic: FAIL (status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("🧪 Sign Language Learning API Test Suite")
    print("="*60)
    
    tests = [
        test_health,
        test_get_all_topics,
        test_get_all_lessons,
        test_get_lessons_by_topic,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            results.append(False)
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
