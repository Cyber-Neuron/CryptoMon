import time

import requests


def get_current_ip():
    """获取当前IP地址"""
    proxies = {"http": "socks5h://127.0.0.1:9050", "https": "socks5h://127.0.0.1:9050"}
    r = requests.get("https://api.myip.com", proxies=proxies)
    return r.json()


def request_new_ip():
    """请求Tor更换新的出口IP"""
    # 通过Tor控制端口发送NEWNYM信号
    control_proxies = {
        "http": "socks5h://127.0.0.1:9051",  # Tor控制端口
        "https": "socks5h://127.0.0.1:9051",
    }
    try:
        # 发送NEWNYM信号
        r = requests.get(
            "http://127.0.0.1:9051/control",
            proxies=control_proxies,
            params={"command": "SIGNAL NEWNYM"},
        )
        if r.status_code == 200:
            print("成功请求新的出口IP")
            # 等待几秒让Tor完成切换
            time.sleep(5)
            return True
        else:
            print(f"请求新IP失败: {r.status_code}")
            return False
    except Exception as e:
        print(f"请求新IP时出错: {e}")
        return False


if __name__ == "__main__":
    # 获取当前IP
    print("当前IP:")
    print(get_current_ip())

    # 请求新IP
    # if request_new_ip() and False:
    #     # 等待切换完成后获取新IP
    #     time.sleep(5)
    #     print("\n新IP:")
    #     print(get_current_ip())
