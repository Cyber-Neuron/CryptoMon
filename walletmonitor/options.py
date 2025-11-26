import requests
import time
import pandas as pd
from datetime import datetime

# 参数配置
INSTRUMENT_NAME = 'ETH-11JUL25-2700-C'
INTERVAL_SECONDS = 3600  # 每小时一次

# 数据存储
history = []

# 获取持仓量和市场摘要
def fetch_summary():
    url = f"https://www.deribit.com/api/v2/public/get_book_summary_by_instrument?instrument_name={INSTRUMENT_NAME}"
    r = requests.get(url).json()
    if 'result' in r and r['result']:
        res = r['result'][0]
        return {
            'timestamp': datetime.utcnow().isoformat(),
            'open_interest': res['open_interest'],
            'last_price': res['last_price'],
            'mark_iv': res.get('mark_iv'),
            'volume': res.get('stats', {}).get('volume'),
            'price_change': res.get('stats', {}).get('price_change'),
        }
    return None

# 主循环
while True:
    try:
        data = fetch_summary()
        if data:
            history.append(data)
            df = pd.DataFrame(history)
            df.to_csv(f"{INSTRUMENT_NAME.replace('-', '_')}_monitor.csv", index=False)
            print(f"[{data['timestamp']}] OI: {data['open_interest']}  Price: {data['last_price']}")
        else:
            print("获取数据失败")
    except Exception as e:
        print("错误:", e)

    time.sleep(INTERVAL_SECONDS)

