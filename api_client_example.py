
# 推荐系统API客户端示例
import requests
import json

API_BASE_URL = "http://127.0.0.1:5000/api"

# 1. 健康检查
response = requests.get(f"{API_BASE_URL}/health")
print("健康检查:", response.json())

# 2. 获取运营商列表
response = requests.get(f"{API_BASE_URL}/carriers")
print("运营商列表:", response.json())

# 3. 获取推荐
recommend_data = {
    "user_needs": {
        "data": 30,
        "calls": 500
    },
    "user_budget": 150
}

response = requests.post(
    f"{API_BASE_URL}/recommend",
    headers={"Content-Type": "application/json"},
    data=json.dumps(recommend_data)
)
print("推荐结果:", response.json())

# 4. 批量推荐
batch_data = {
    "requests": [
        {
            "user_needs": {"data": 20, "calls": 300},
            "user_budget": 100
        },
        {
            "user_needs": {"data": 50, "calls": 800},
            "user_budget": 200
        }
    ]
}

response = requests.post(
    f"{API_BASE_URL}/batch-recommend",
    headers={"Content-Type": "application/json"},
    data=json.dumps(batch_data)
)
print("批量推荐结果:", response.json())
