import hashlib
import json
import random
import re
import time
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

import requests


def random_cache_ts():
    """生成随机的时间戳"""
    return str(int(time.time() * 1000)) + str(random.randint(0, 999)).zfill(3)


def random_platform():
    """随机选择平台信息"""
    platforms = [
        {"platform": '"macOS"', "os": "Mac OS X"},
        {"platform": '"Windows"', "os": "Windows NT 10.0"},
        {"platform": '"Linux"', "os": "X11; Linux x86_64"},
    ]
    return random.choice(platforms)


def random_user_agent(os_info):
    """生成随机的User-Agent"""
    chrome_ver = random.randint(110, 140)
    safari_ver = random.randint(500, 600)

    if os_info["platform"] == '"macOS"':
        mac_ver = f"{10 + random.randint(0, 5)}_{15 + random.randint(0, 5)}_{7 + random.randint(0, 5)}"
        os_str = f"Macintosh; Intel Mac OS X {mac_ver}"
    elif os_info["platform"] == '"Windows"':
        os_str = "Windows NT 10.0; Win64; x64"
    else:  # Linux
        os_str = "X11; Linux x86_64"

    return f"Mozilla/5.0 ({os_str}) AppleWebKit/{safari_ver}.36 (KHTML, like Gecko) Chrome/{chrome_ver}.0.0.0 Safari/{safari_ver}.36"


def get_random_headers():
    """生成完整的随机headers"""
    platform_info = random_platform()
    user_agent = random_user_agent(platform_info)

    return {
        "accept": "*/*",
        "accept-language": "en",
        "origin": "https://intel.arkm.com",
        "sec-ch-ua": f'"Google Chrome";v="{random.randint(110, 140)}", "Chromium";v="{random.randint(110, 140)}", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": platform_info["platform"],
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": user_agent,
        "Accept": "application/json, text/plain, */*",
        "Referer": "https://intel.arkm.com/",
    }


def fetch_client_key(session, proxies=None):
    """访问首页，提取clientKey"""
    url = "https://intel.arkm.com/"
    resp = session.get(url, proxies=proxies, timeout=30)
    m = re.search(r'"clientKey"\s*:\s*"([a-zA-Z0-9]+)"', resp.text)
    if not m:
        raise Exception("无法找到 clientKey")
    return m.group(1)


def gen_arkham_headers(api_path, client_key):
    """生成X-Timestamp和X-Payload"""
    ts = str(int(time.time()))  # 使用当前时间戳
    p1 = f"{api_path}:{ts}:{client_key}"
    r = hashlib.sha256(p1.encode()).hexdigest()
    p2 = f"{client_key}:{r}"
    payload = hashlib.sha256(p2.encode()).hexdigest()
    return {
        "X-Timestamp": ts,
        "X-Payload": payload,
    }


def arkham_get(api_path, proxies=None):
    """发起请求"""
    with requests.Session() as s:
        # 使用随机headers
        s.headers.update(get_random_headers())

        if proxies:
            s.proxies.update(proxies)

        # 必须走logout，保证干净session
        s.get("https://intel.arkm.com/")
        # s.post('https://intel.arkm.com/api/logout')

        # 拿到clientKey
        client_key = fetch_client_key(s, proxies)
        auth_headers = gen_arkham_headers(api_path, client_key)
        s.headers.update(auth_headers)

        api_url = f"https://api.arkm.com{api_path}"
        resp = s.get(api_url)
        print("Status:", resp.status_code)
        print("Headers:", resp.headers)
        print("Body:", resp.text)
        return resp


def parse_har_file(har_file_path: str) -> List[Dict[str, Any]]:
    """解析HAR文件，提取arkm.com的请求记录"""
    with open(har_file_path, "r", encoding="utf-8") as f:
        har_data = json.load(f)

    arkm_requests = []
    for entry in har_data["log"]["entries"]:
        url = entry["request"]["url"]
        if "arkm.com" in url:
            request = {
                "url": url,
                "method": entry["request"]["method"],
                "headers": {h["name"]: h["value"] for h in entry["request"]["headers"]},
                "post_data": entry["request"].get("postData", {}).get("text", ""),
                "timestamp": entry["startedDateTime"],
            }
            arkm_requests.append(request)

    return arkm_requests


def simulate_request_sequence(
    requests: List[Dict[str, Any]], proxies: Optional[Dict[str, str]] = None
):
    """模拟请求序列"""
    session = requests.Session()
    session.headers.update(get_random_headers())

    if proxies:
        session.proxies.update(proxies)

    # 首先访问首页获取clientKey
    session.get("https://intel.arkm.com/")
    client_key = fetch_client_key(session, proxies)

    for req in requests:
        url = req["url"]
        method = req["method"]
        headers = req["headers"]
        post_data = req["post_data"]

        # 解析API路径
        parsed_url = urlparse(url)
        api_path = parsed_url.path

        # 生成认证headers
        auth_headers = gen_arkham_headers(api_path, client_key)

        # 更新headers
        current_headers = get_random_headers()
        current_headers.update(
            {
                "Accept": "application/json, text/plain, */*",
                "Referer": "https://intel.arkm.com/",
            }
        )
        current_headers.update(auth_headers)

        # 发起请求
        try:
            if method == "GET":
                response = session.get(url, headers=current_headers)
            elif method == "POST":
                response = session.post(url, headers=current_headers, data=post_data)
            else:
                print(f"Unsupported method: {method}")
                continue

            print(f"\nRequest: {method} {url}")
            print(f"Status: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print(f"Response Body: {response.text[:200]}...")  # 只打印前200个字符

            # 添加随机延迟，模拟真实用户行为
            time.sleep(random.uniform(1, 3))

        except Exception as e:
            print(f"Error processing request {url}: {str(e)}")


if __name__ == "__main__":
    proxies = {
        "http": "socks5h://127.0.0.1:9050",
        "https": "socks5h://127.0.0.1:9050",
    }
    api_path = "/intelligence/address/0x31FbEe2B22E65dE59d16b36e83A224e984F5347E"
    arkham_get(api_path, proxies)
