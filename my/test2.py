import httpx
import asyncio

import fake_useragent

async def test_douyin_request():
    # share_url = "https://www.iesdouyin.com/share/video/7587477312384601401"
    #
    # # 定义默认请求头
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1 OPT/4.2.3',
    # }
    #
    # async with httpx.AsyncClient(follow_redirects=True) as client:
    #     response = await client.get(share_url, headers=headers)
    #     response.raise_for_status()
    #
    #     print(f"Status Code: {response.status_code}")
    #     print(f"Response URL: {response.url}")
    #     print(f"Response Length: {len(response.content)}")
    #     print(f"Response data: {response.text}")
    #
    #     return response


    print(f"fake_useragent: " + fake_useragent.UserAgent(os=["windows"]).random)
    print(f"fake_useragent: " + fake_useragent.UserAgent(os=["windows"]).random)
    print(f"fake_useragent: " + fake_useragent.UserAgent(os=["windows"]).random)
    print(f"fake_useragent: " + fake_useragent.UserAgent(os=["windows"]).random)
    print(f"fake_useragent: " + fake_useragent.UserAgent(os=["windows"]).random)
    print(f"fake_useragent: " + fake_useragent.UserAgent(os=["windows"]).random)

# 运行异步函数
if __name__ == "__main__":
    asyncio.run(test_douyin_request())