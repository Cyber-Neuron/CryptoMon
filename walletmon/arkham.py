import hashlib
import json
import logging
import os
import random
import re
import time
from datetime import datetime, timezone

import fire
import pytz
import requests
from db_utils import get_db_connection, get_or_create_wallet, store_transactions
from psycopg2.extras import DictCursor

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
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050",
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

            return response

        except Exception as e:
            # If any error occurs, reinitialize session for next request
            self._initialize_session(refresh=True)
            raise e

    def get_transfers(
        self,
        base="binance",
        tokens="usd-coin,tether",
        flow="out",
        chains=None,
        from_addresses=None,
        to_addresses=None,
        counterparties=None,
        time_last=None,
        time_gte=None,
        time_lte=None,
        value_gte=None,
        value_lte=None,
        usd_gte=None,
        usd_lte=None,
        sort_key="time",
        sort_dir="desc",
        limit=50,
        offset=0,
    ):
        """Get transaction history from Arkham API.

        Args:
            base: Filter by specific entity or address. For example, "0x123abc" or "binance".
            tokens: Comma-separated list of token addresses or token IDs.
            flow: Direction of the transfer. Valid values are "in", "out", "self", or "all".
            chains: Comma-separated list of chains (e.g. "ethereum,bsc").
            from_addresses: Comma-separated list of addresses for the 'from' side.
            to_addresses: Comma-separated list of addresses for the 'to' side.
            counterparties: Comma-separated list of addresses to treat as counterparties.
            time_last: Filter transfers from a recent duration (e.g. "24h").
            time_gte: Filter from a specific timestamp in milliseconds.
            time_lte: Filter to a specific timestamp in milliseconds.
            value_gte: Minimum raw token amount.
            value_lte: Maximum raw token amount.
            usd_gte: Minimum USD value.
            usd_lte: Maximum USD value.
            sort_key: Field to sort by ("time", "value", or "usd").
            sort_dir: Sort direction ("asc" or "desc").
            limit: Maximum number of results (default 50).
            offset: Pagination offset (default 0).
        """
        api_path = f"/transfers"
        querystring = {
            "base": base,
            "tokens": tokens,
            "flow": flow,
        }

        # Add optional parameters if they are provided
        if chains:
            querystring["chains"] = chains
        if from_addresses:
            querystring["from"] = from_addresses
        if to_addresses:
            querystring["to"] = to_addresses
        if counterparties:
            querystring["counterparties"] = counterparties
        if time_last:
            querystring["timeLast"] = time_last
        if time_gte:
            querystring["timeGte"] = time_gte
        if time_lte:
            querystring["timeLte"] = time_lte
        if value_gte:
            querystring["valueGte"] = value_gte
        if value_lte:
            querystring["valueLte"] = value_lte
        if usd_gte:
            querystring["usdGte"] = usd_gte
        if usd_lte:
            querystring["usdLte"] = usd_lte
        if sort_key:
            querystring["sortKey"] = sort_key
        if sort_dir:
            querystring["sortDir"] = sort_dir
        if limit:
            querystring["limit"] = str(limit)
        if offset:
            querystring["offset"] = str(offset)

        auth_headers = self._gen_arkham_headers(api_path)
        self.session.headers.update(auth_headers)
        api_url = f"https://api.arkm.com{api_path}"
        response = self.session.get(api_url, params=querystring)

        # Convert timestamps to YYYYMMDDHHmm format for filename
        # time_str = ""
        # if time_gte and time_lte:
        #     time_gte_str = datetime.fromtimestamp(time_gte / 1000).strftime(
        #         "%Y%m%d%H%M"
        #     )
        #     time_lte_str = datetime.fromtimestamp(time_lte / 1000).strftime(
        #         "%Y%m%d%H%M"
        #     )
        #     time_str = f"_{time_gte_str}_{time_lte_str}"

        # try:
        #     json.dump(
        #         response.json(),
        #         open(
        #             f"arkham_transfers_{time.time()}_{flow}_{chains}_{tokens}{time_str}.json",
        #             "w",
        #         ),
        #     )
        # except Exception as e:
        #     print(e)
        return response

    def extract_wallets(self, response, base):
        base_wallets = []
        for record in response.json().get("transfers", []):
            from_wallet_name = (
                record.get("fromAddress", {}).get("arkhamEntity", {}).get("name", "")
            )
            from_wallet_label = (
                record.get("fromAddress", {}).get("arkhamLabel", {}).get("name", "")
            )
            to_wallet_name = (
                record.get("toAddress", {}).get("arkhamEntity", {}).get("name", "")
            )
            to_wallet_label = (
                record.get("toAddress", {}).get("arkhamLabel", {}).get("name", "")
            )
            if (
                base in from_wallet_name.lower()
                or base in to_wallet_name.lower()
                or "gate" in from_wallet_name.lower()
                or "gate" in to_wallet_name.lower()
            ):
                wallet = {
                    "address": (
                        record.get("fromAddress", {}).get("address")
                        if base in from_wallet_name.lower()
                        else record.get("toAddress", {}).get("address")
                    ),
                    "value": record.get("unitValue"),
                    "usd_value": record.get("historicalUSD"),
                    "name": (
                        from_wallet_name + " " + from_wallet_label
                        if base in from_wallet_name.lower()
                        else to_wallet_name + " " + to_wallet_label
                    ),
                }
                base_wallets.append(wallet)

        return base_wallets

    def update_top_wallets(
        self,
        limit=16,
        value_gte=100,
        tokens="ethereum",
        time_last="24h",
        base="binance",
        flow="all",
        sort_key="time",
        sort_dir="desc",
    ):
        # https://api.arkm.com/transfers?base=binance&flow=all&sortKey=time&sortDir=desc&limit=16&offset=16&valueGte=100&tokens=ethereum&timeLast=7d
        total_records = 0
        wallets = []
        resp = self.get_transfers(
            base=base,
            flow=flow,
            sort_key=sort_key,
            sort_dir=sort_dir,
            limit=limit,
            offset=0,
            value_gte=value_gte,
            tokens=tokens,
            time_last=time_last,
        )
        wallets = self.extract_wallets(resp, base)
        total_records = resp.json().get("count")
        logger.info(f"Total records: {total_records}")
        for i in range(0, total_records, limit):
            if i > 0:
                resp = self.get_transfers(
                    base=base,
                    flow=flow,
                    sort_key=sort_key,
                    sort_dir=sort_dir,
                    limit=limit,
                    offset=i,
                    value_gte=value_gte,
                    tokens=tokens,
                    time_last=time_last,
                )
                tmp_wallets = self.extract_wallets(resp, base)
                wallets.extend(tmp_wallets)
                logger.info(f"Updated {len(tmp_wallets)} wallets")
                time.sleep(1)
        uniq_wallets = {}
        with get_db_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                for wallet in wallets:
                    if wallet["address"] not in uniq_wallets:
                        uniq_wallets[wallet["address"]] = wallet
                        get_or_create_wallet(
                            cur,
                            wallet["address"],
                            wallet["name"],
                            grp_name=base,
                            grp_type="Hot2",
                        )
                conn.commit()

    def extract_transations(self, response):
        """Extract transactions from the response."""
        transaction_data_records = []
        for record in response.get("transfers", []):
            # print(type(record), record.keys())
            transaction_data = {
                "hash": record.get("transactionHash"),
                "from": record.get("fromAddress", {}).get("address"),
                "chain": record.get("fromAddress", {}).get("chain"),
                "from_label": (
                    record.get("fromAddress", {}).get("arkhamLabel", {}).get("name")
                ),
                "from_entity": (
                    record.get("fromAddress", {}).get("arkhamEntity", {}).get("name")
                ),
                "from_type": (
                    record.get("fromAddress", {}).get("arkhamEntity", {}).get("type")
                ),
                "to": record.get("toAddress", {}).get("address"),
                "to_label": (
                    record.get("toAddress", {}).get("arkhamLabel", {}).get("name")
                ),
                "to_entity": (
                    record.get("toAddress", {}).get("arkhamEntity", {}).get("name")
                ),
                "to_type": (
                    record.get("toAddress", {}).get("arkhamEntity", {}).get("type")
                ),
                "token": (
                    "ETH"
                    if record.get("tokenName", "").lower() == "ethereum"
                    else record.get("tokenName")
                ),
                "block_number": record.get("blockNumber"),
                "amount": record.get("unitValue"),
                "timestamp": record.get("blockTimestamp"),
                "usd_value": record.get("historicalUSD"),
                "raw_data": record,
            }
            transaction_data_records.append(transaction_data)
        return transaction_data_records

    def get_token_flow_stats(
        self,
        token,
        time_last="24h",
        interval_minutes=60,
        base="binance",
        chains=None,
        usd_gte=100000,
        time_gte=None,
        time_lte=None,
        store_to_db=False,
    ):
        """Calculate token flow statistics for a specific time period.

        Args:
            token: Token symbol or address (e.g. "usd-coin" or "0x...")
            time_last: Time period to analyze (e.g. "24h", "7d", "30d")
            interval_minutes: Time interval for grouping data (default 60 minutes)
            base: Base entity or address to analyze
            chains: Comma-separated list of chains to include
            usd_gte: Minimum USD value to include
        """
        # Get inflow data
        inflow_response = self.get_transfers(
            base=base,
            tokens=token,
            flow="in",
            chains=chains,
            time_last=time_last,
            limit=50,  # Get maximum results
            usd_gte=usd_gte,
            time_gte=time_gte,
            time_lte=time_lte,
        )
        inflow_data = inflow_response.json()
        inflow_transactions = self.extract_transations(inflow_data)
        if store_to_db:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    filtered_inflow_hashs = store_transactions(cur, inflow_transactions)
                    conn.commit()

        # Get outflow data
        outflow_response = self.get_transfers(
            base=base,
            tokens=token,
            flow="out",
            chains=chains,
            time_last=time_last,
            limit=50,  # Get maximum results
            usd_gte=usd_gte,
            time_gte=time_gte,
            time_lte=time_lte,
        )
        outflow_data = outflow_response.json()
        outflow_transactions = self.extract_transations(outflow_data)
        if store_to_db:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=DictCursor) as cur:
                    filtered_outflow_hashs = store_transactions(
                        cur, outflow_transactions
                    )
                    conn.commit()

        # Initialize statistics
        stats = {
            "total_inflow": 0,
            "total_outflow": 0,
            "interval_stats": [],
            "total_inflow_usd": 0,
            "total_outflow_usd": 0,
        }

        # Process inflow data
        for transfer in inflow_data.get("transfers", []):
            if transfer.get("transactionHash") in filtered_inflow_hashs:
                logger.info(f"skipping inflow {transfer.get('transactionHash')}")
                continue
            value = float(transfer.get("unitValue", 0))
            historicalUSD = float(transfer.get("historicalUSD", 0))
            # Parse UTC timestamp and convert to local timezone
            utc_time = datetime.strptime(
                transfer.get("blockTimestamp", ""), "%Y-%m-%dT%H:%M:%SZ"
            )
            utc_time = utc_time.replace(tzinfo=pytz.UTC)
            local_time = utc_time.astimezone()
            timestamp = int(utc_time.timestamp())

            stats["total_inflow"] += value
            stats["total_inflow_usd"] += historicalUSD
            # Add to interval stats
            interval_time = (timestamp // (interval_minutes * 60)) * (
                interval_minutes * 60
            )
            found = False
            for interval in stats["interval_stats"]:
                if interval["timestamp"] == interval_time:
                    interval["inflow"] += value
                    interval["inflow_count"] += 1
                    interval["inflow_usd"] += historicalUSD
                    found = True
                    break
            if not found:
                stats["interval_stats"].append(
                    {
                        "timestamp": interval_time,
                        "inflow": value,
                        "outflow": 0,
                        "inflow_count": 1,
                        "outflow_count": 0,
                        "inflow_usd": historicalUSD,
                        "outflow_usd": 0,
                    }
                )

        # Process outflow data
        for transfer in outflow_data.get("transfers", []):
            if transfer.get("transactionHash") in filtered_outflow_hashs:
                logger.info(f"skipping outflow {transfer.get('transactionHash')}")
                continue
            value = float(transfer.get("unitValue", 0))
            historicalUSD = float(transfer.get("historicalUSD", 0))
            # Parse UTC timestamp and convert to local timezone
            utc_time = datetime.strptime(
                transfer.get("blockTimestamp", ""), "%Y-%m-%dT%H:%M:%SZ"
            )
            utc_time = utc_time.replace(tzinfo=pytz.UTC)
            local_time = utc_time.astimezone()
            timestamp = int(utc_time.timestamp())

            stats["total_outflow"] += value
            stats["total_outflow_usd"] += historicalUSD
            # Add to interval stats
            interval_time = (timestamp // (interval_minutes * 60)) * (
                interval_minutes * 60
            )
            found = False
            for interval in stats["interval_stats"]:
                if interval["timestamp"] == interval_time:
                    interval["outflow"] += value
                    interval["outflow_count"] += 1
                    interval["outflow_usd"] += historicalUSD
                    found = True
                    break
            if not found:
                stats["interval_stats"].append(
                    {
                        "timestamp": interval_time,
                        "inflow": 0,
                        "outflow": value,
                        "inflow_count": 0,
                        "outflow_count": 1,
                        "inflow_usd": 0,
                        "outflow_usd": historicalUSD,
                    }
                )

        # Sort intervals by timestamp
        stats["interval_stats"].sort(key=lambda x: x["timestamp"])

        return stats

    def analyze_from_file(self, file_path, interval_minutes=60):
        """Analyze token flow statistics from a local JSON file.

        Args:
            file_path: Path to the JSON file containing transfer data
            interval_minutes: Time interval for grouping data (default 60 minutes)

        Returns:
            dict: Statistics containing:
                - total_inflow: Total amount of tokens flowing in
                - total_outflow: Total amount of tokens flowing out
                - interval_stats: List of dicts containing per-interval statistics
        """
        import ast
        import json

        # Read and parse the JSON file
        with open(file_path, "r") as f:
            content = f.read()
            # Convert single quotes to double quotes for valid JSON
            content = content.replace("'", '"')
            # Handle None values
            content = content.replace('"None"', "null")
            data = json.loads(content)

        # Initialize statistics
        stats = {"total_inflow": 0, "total_outflow": 0, "interval_stats": []}

        # Process transfers
        for transfer in data.get("transfers", []):
            value = float(transfer.get("unitValue", 0))
            # Parse UTC timestamp and convert to local timezone
            utc_time = datetime.strptime(
                transfer.get("blockTimestamp", ""), "%Y-%m-%dT%H:%M:%SZ"
            )
            utc_time = utc_time.replace(tzinfo=pytz.UTC)
            local_time = utc_time.astimezone()
            timestamp = int(local_time.timestamp())

            # Determine if it's inflow or outflow based on the from/to addresses
            is_inflow = False
            is_outflow = False

            # Check if the transfer involves Binance
            from_address = transfer.get("fromAddress", {})
            to_address = transfer.get("toAddress", {})

            if from_address.get("arkhamEntity", {}).get("id") == "binance":
                is_outflow = True
            elif to_address.get("arkhamEntity", {}).get("id") == "binance":
                is_inflow = True

            if is_inflow:
                stats["total_inflow"] += value
            elif is_outflow:
                stats["total_outflow"] += value

            # Add to interval stats
            interval_time = (timestamp // (interval_minutes * 60)) * (
                interval_minutes * 60
            )
            found = False
            for interval in stats["interval_stats"]:
                if interval["timestamp"] == interval_time:
                    if is_inflow:
                        interval["inflow"] += value
                        interval["inflow_count"] += 1
                    elif is_outflow:
                        interval["outflow"] += value
                        interval["outflow_count"] += 1
                    found = True
                    break
            if not found:
                new_interval = {
                    "timestamp": interval_time,
                    "inflow": value if is_inflow else 0,
                    "outflow": value if is_outflow else 0,
                    "inflow_count": 1 if is_inflow else 0,
                    "outflow_count": 1 if is_outflow else 0,
                }
                stats["interval_stats"].append(new_interval)

        # Sort intervals by timestamp
        stats["interval_stats"].sort(key=lambda x: x["timestamp"])

        return stats

    def analyze_flows(
        self,
        token,
        time_last="24h",
        interval_minutes=60,
        usd_gte=100000,
        chains="ethereum",
        time_gte=None,
        time_lte=None,
        export_csv=True,
        store_to_db=False,
    ):
        """Analyze token flows using API.

        Args:
            token: Token symbol (e.g. "usd-coin")
            time_last: Time period to analyze (e.g. "24h", "7d")
            interval_minutes: Time interval for grouping data
            usd_gte: Minimum USD value to include
            chains: Comma-separated list of chains
            time_gte: Start time in YYYYMMDDHHmm format (e.g. "202403011630" for 2024-03-01 16:30)
            time_lte: End time in YYYYMMDDHHmm format (e.g. "202403021630" for 2024-03-02 16:30)
            export_csv: Whether to export transaction data to CSV (default: True)
            store_to_db: Whether to store transactions in database (default: False)
        """
        self.proxies = {
            "http": "socks5h://127.0.0.1:9050",
            "https": "socks5h://127.0.0.1:9050",
        }
        self._initialize_session()

        # Initialize combined stats
        combined_stats = {
            "total_inflow": 0,
            "total_outflow": 0,
            "total_inflow_usd": 0,
            "total_outflow_usd": 0,
            "interval_stats": [],
        }

        # Convert time_gte and time_lte from YYYYMMDDHHmm to UTC milliseconds if provided
        if time_gte:
            try:
                # Parse local time
                local_time_gte = datetime.strptime(str(time_gte), "%Y%m%d%H%M")
                # Convert to UTC
                utc_time_gte = local_time_gte.astimezone(pytz.UTC)
                time_gte_ms = int(utc_time_gte.timestamp() * 1000)
                print(f"Local time {local_time_gte} converted to UTC {utc_time_gte}")
            except ValueError:
                raise ValueError(
                    "time_gte must be in YYYYMMDDHHmm format (e.g. 202403011630)"
                )
        else:
            time_gte_ms = None

        if time_lte:
            try:
                # Parse local time
                local_time_lte = datetime.strptime(str(time_lte), "%Y%m%d%H%M")
                # Convert to UTC
                utc_time_lte = local_time_lte.astimezone(pytz.UTC)
                time_lte_ms = int(utc_time_lte.timestamp() * 1000)
                print(f"Local time {local_time_lte} converted to UTC {utc_time_lte}")
            except ValueError:
                raise ValueError(
                    "time_lte must be in YYYYMMDDHHmm format (e.g. 202403021630)"
                )
        else:
            time_lte_ms = None

        # If time_gte and time_lte are provided, split into hourly intervals
        if time_gte_ms and time_lte_ms:
            current_time = time_gte_ms
            while current_time < time_lte_ms:
                # Calculate end time for this interval (1 hour later or time_lte)
                interval_end = min(current_time + (60 * 60 * 1000), time_lte_ms)

                # Convert UTC timestamps back to local time for display
                local_start = datetime.fromtimestamp(current_time / 1000).astimezone()
                local_end = datetime.fromtimestamp(interval_end / 1000).astimezone()
                print(f"Fetching data from {local_start} to {local_end}")

                # Get stats for this interval
                interval_stats = self.get_token_flow_stats(
                    token=token,
                    time_last="",  # Empty string instead of None when we have specific time range
                    interval_minutes=interval_minutes,
                    usd_gte=usd_gte,
                    chains=chains,
                    time_gte=current_time,
                    time_lte=interval_end,
                    store_to_db=store_to_db,
                )

                # Merge stats
                combined_stats["total_inflow"] += interval_stats["total_inflow"]
                combined_stats["total_outflow"] += interval_stats["total_outflow"]
                combined_stats["total_inflow_usd"] += interval_stats["total_inflow_usd"]
                combined_stats["total_outflow_usd"] += interval_stats[
                    "total_outflow_usd"
                ]
                combined_stats["interval_stats"].extend(
                    interval_stats["interval_stats"]
                )

                # Move to next hour
                current_time = interval_end

                # Add a small delay to avoid rate limiting
                time.sleep(1)
        else:
            # If no specific time range, use time_last parameter
            combined_stats = self.get_token_flow_stats(
                token=token,
                time_last=time_last,
                interval_minutes=interval_minutes,
                usd_gte=usd_gte,
                chains=chains,
                time_gte=time_gte_ms,
                time_lte=time_lte_ms,
                store_to_db=store_to_db,
            )

        # Sort all interval stats by timestamp
        combined_stats["interval_stats"].sort(key=lambda x: x["timestamp"])
        self._print_stats(combined_stats)

        # Export to CSV if requested
        if export_csv:
            # Generate filename based on time range if available
            if time_gte and time_lte:
                output_file = (
                    f"arkham_transactions{chains}_{token}_{time_gte}_{time_lte}.csv"
                )
            else:
                output_file = None
            self.export_to_csv(combined_stats, output_file)

        return combined_stats

    def analyze_file(self, file_path, interval_minutes=60):
        """Analyze token flows from a local JSON file.

        Args:
            file_path: Path to the JSON file
            interval_minutes: Time interval for grouping data
        """
        stats = self.analyze_from_file(file_path, interval_minutes)
        self._print_stats(stats)
        return stats

    def _print_stats(self, stats):
        """Print statistics in a formatted way."""
        print("\n=== Token Flow Statistics ===")
        print(f"Total Inflow: {stats['total_inflow']:,.5f}")
        print(f"Total Outflow: {stats['total_outflow']:,.5f}")
        print(f"Net Flow: {stats['total_inflow'] - stats['total_outflow']:,.5f}")
        print(f"Total Inflow USD: {stats['total_inflow_usd']:,.5f}")
        print(f"Total Outflow USD: {stats['total_outflow_usd']:,.5f}")
        print(
            f"Net Flow USD: {stats['total_inflow_usd'] - stats['total_outflow_usd']:,.5f}"
        )

        print("\nTime Interval Statistics:")
        for interval in stats["interval_stats"]:
            # Convert UTC timestamp to local timezone
            local_time = datetime.fromtimestamp(
                interval["timestamp"], tz=pytz.UTC
            ).astimezone()
            print(f"\nTime: {local_time.strftime('%Y-%m-%d %H:%M %Z')}")
            print(
                f"  Inflow: {interval['inflow']:,.5f} (Count: {interval['inflow_count']})"
            )
            print(
                f"  Outflow: {interval['outflow']:,.5f} (Count: {interval['outflow_count']})"
            )
            print(f"  Net Flow: {interval['inflow'] - interval['outflow']:,.5f}")

    def export_to_csv(self, stats, output_file=None):
        """Export transaction data to CSV format.

        Args:
            stats: Statistics dictionary containing transaction data
            output_file: Optional output file path. If not provided, will use timestamp in filename.

        Returns:
            Path to the generated CSV file
        """
        import csv
        from datetime import datetime

        # Generate default filename if not provided
        if not output_file:
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            output_file = f"arkham_transactions_{timestamp}.csv"

        # Extract all transactions from interval_stats
        transactions = []
        for interval in stats["interval_stats"]:
            # Get the timestamp for this interval
            timestamp = datetime.fromtimestamp(interval["timestamp"], tz=timezone.utc)
            # print(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
            # Add inflow transactions
            if interval["inflow"] > 0:
                transactions.append(
                    {
                        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "from": "External",
                        "to": "Binance",
                        "amount": interval["inflow"],
                        "usd_amount": interval["inflow_usd"],
                        "type": "inflow",
                    }
                )

            # Add outflow transactions (with negative values)
            if interval["outflow"] > 0:
                transactions.append(
                    {
                        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                        "from": "Binance",
                        "to": "External",
                        "amount": -interval["outflow"],  # Convert to negative
                        "usd_amount": -interval["outflow_usd"],  # Convert to negative
                        "type": "outflow",
                    }
                )

        # Sort transactions by timestamp
        transactions.sort(key=lambda x: x["timestamp"])

        # Write to CSV
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["timestamp", "from", "to", "amount", "usd_amount", "type"],
            )
            writer.writeheader()
            writer.writerows(transactions)

        print(f"\nTransaction data has been exported to: {output_file}")
        return output_file


if __name__ == "__main__":
    import fire

    # Example usage:
    # python arkham.py analyze_flows --token="usd-coin" --time_last="1h" --interval_minutes=10 --use_proxy
    # python arkham.py analyze_file --file_path="exchange_monitor/tmp.json" --interval_minutes=10
    logging.basicConfig(level=logging.INFO)
    # fire.Fire(ArkhamClient)
    client = ArkhamClient()
    value_gte_filters = {
        "usd-coin": 100000,
        "tether": 100000,
        "ethereum": 100,
    }
    bases = [
        "bybit",
        "binance",
        "okx",
        "coinbase",
        "kraken",
        "aave",
        "gate-io",
        "cumberland",
    ]
    bases = ["cumberland"]
    for base in bases:
        for token, value_gte in value_gte_filters.items():
            print(f"Analyzing {token} with value_gte={value_gte} on {base}")
            client.update_top_wallets(
                limit=16,
                value_gte=value_gte,
                tokens=token,
                time_last="1d",
                base=base,
                flow="all",
                sort_key="time",
                sort_dir="desc",
            )
