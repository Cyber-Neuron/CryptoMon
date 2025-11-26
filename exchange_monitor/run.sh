#!/bin/bash

# 设置时间范围变量
TIME_START="202506170000"
TIME_END="202506172200"

# 运行分析
python arkham.py analyze_flows --token="ethereum" --time_last="1h" --interval_minutes=10 --usd_gte=100000 --time-gte=$TIME_START --time-lte=$TIME_END
python arkham.py analyze_flows --token="usd-coin" --time_last="1h" --interval_minutes=10 --usd_gte=100000 --time-gte=$TIME_START --time-lte=$TIME_END
python arkham.py analyze_flows --token="tether" --time_last="1h" --interval_minutes=10 --usd_gte=100000 --time-gte=$TIME_START --time-lte=$TIME_END
