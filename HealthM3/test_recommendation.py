import requests
import json

def test_recommendation():
    # 登录获取token
    login_url = "http://localhost:5000/api/auth/login"
    login_data = {
        "username": "test_user",
        "password": "test123"
    }
    print("正在发送登录请求...")
    login_response = requests.post(login_url, json=login_data)
    print("登录响应状态码:", login_response.status_code)
    print("登录响应内容:", login_response.text)
    
    if login_response.status_code == 200:
        login_data = login_response.json()
        if 'token' in login_data:
            token = login_data['token']
            user_id = login_data['user']['id']
            
            # 测试推荐API
            headers = {
                "Authorization": f"Bearer {token}"
            }
            recommendation_url = f"http://localhost:5000/api/health/recommendation/{user_id}"
            print("\n正在发送推荐请求...")
            recommendation_response = requests.get(recommendation_url, headers=headers)
            print("推荐响应状态码:", recommendation_response.status_code)
            print("推荐响应内容:", recommendation_response.text)
        else:
            print("登录响应中没有token")
    else:
        print("登录失败")

if __name__ == "__main__":
    test_recommendation() 