import hashlib
import logging
import os
import random
import re
import time

import requests

logger = logging.getLogger(__name__)


def random_cache_ts():
    """生成随机的时间戳"""
    return str(int(time.time() * 50)) + str(random.randint(0, 999)).zfill(3)


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
    # intelligence/address/0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549
    return {
        "accept": "*/*",
        "accept-language": "en",
        "origin": "https://intel.arkm.com",
        # "referer": "https://intel.arkm.com/explorer/address/0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549",
        "sec-ch-ua": f'"Google Chrome";v="{random.randint(110, 140)}", "Chromium";v="{random.randint(110, 140)}", "Not/A)Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": platform_info["platform"],
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": user_agent,
    }


class ArkhamClient:
    def __init__(self, use_proxy=True):
        """Initialize Arkham client with session and authentication.

        Args:
            use_proxy: Whether to use proxy (default: False)
        """
        # self.proxies = None
        # if use_proxy:
        self.proxies = {
            "http": "socks5h://tor:9050",
            "https": "socks5h://tor:9050",
        }
        self.session = None
        self.client_key = None
        self._initialize_session()

    def _initialize_session(self, refresh=False):
        """Initialize or reinitialize the session with fresh authentication."""
        if self.session:
            self.session.close()

        self.session = requests.Session()
        self.session.headers.update(get_random_headers())
        self.session.headers.update(
            {
                "Accept": "application/json, text/plain, */*",
                "Referer": "https://intel.arkm.com/",
            }
        )

        if self.proxies:
            self.session.proxies.update(self.proxies)

        # Get client key
        self.client_key = self._fetch_client_key(refresh)

    def _within_24h(self):
        if os.path.exists("client_key.txt"):
            return os.path.getmtime("client_key.txt") > (time.time() - 3600 * 24)
        return False

    def _fetch_client_key(self, refresh=False):
        """Fetch client key from the homepage."""
        if refresh or not os.path.exists("client_key.txt") or not self._within_24h():
            print(
                "获取新的 client_key",
                refresh,
                os.path.exists("client_key.txt"),
                self._within_24h(),
            )
            url = "https://intel.arkm.com/"
            resp = self.session.get(url, timeout=30)
            m = re.search(r'"clientKey"\s*:\s*"([a-zA-Z0-9]+)"', resp.text)
            if not m:
                raise Exception("无法找到 clientKey")
            with open("client_key.txt", "w") as f:
                f.write(m.group(1))
            return m.group(1)
        else:
            print("使用缓存的 client_key")
            with open("client_key.txt", "r") as f:
                return f.read()

    def _gen_arkham_headers(self, api_path):
        """Generate X-Timestamp and X-Payload headers."""
        ts = str(int(time.time()))
        p1 = f"{api_path}:{ts}:{self.client_key}"
        r = hashlib.sha256(p1.encode()).hexdigest()
        p2 = f"{self.client_key}:{r}"
        payload = hashlib.sha256(p2.encode()).hexdigest()
        return {
            "X-Timestamp": ts,
            "X-Payload": payload,
        }

    def get_address_info(self, address):
        """Get address information from Arkham API.

        Args:
            address: The wallet address to query

        Returns:
            Response object from the API
        """
        api_path = f"/intelligence/address/{address}"

        try:
            # Update headers for this request
            auth_headers = self._gen_arkham_headers(api_path)
            self.session.headers.update(auth_headers)

            # Make the request
            api_url = f"https://api.arkm.com{api_path}"
            response = self.session.get(api_url)

            # Check for invalid timestamp error
            if (
                response.status_code == 400
                and "invalid timestamp format" in response.text
            ):
                # Reinitialize session and retry once
                self._initialize_session(refresh=True)
                auth_headers = self._gen_arkham_headers(api_path)
                self.session.headers.update(auth_headers)
                response = self.session.get(api_url)

            return response.json()

        except Exception as e:
            # If any error occurs, reinitialize session for next request
            self._initialize_session(refresh=True)
            raise e
