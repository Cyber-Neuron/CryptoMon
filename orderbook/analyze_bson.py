#!/usr/bin/env python3
"""
BSON数据分析工具
用于分析币安交易数据的BSON文件
"""

import argparse
import json
import os
from collections import defaultdict
from datetime import datetime

import bson


def read_bson_file(filename):
    """读取BSON文件中的所有记录"""
    records = []
    try:
        with open(filename, "rb") as f:
            while True:
                try:
                    record = bson.loads(f.read())
                    records.append(record)
                except EOFError:
                    break
                except Exception as e:
                    print(f"读取记录时出错: {e}")
                    break
    except Exception as e:
        print(f"打开文件 {filename} 时出错: {e}")
    return records


def analyze_trades(records):
    """分析交易数据"""
    if not records:
        print("没有找到交易记录")
        return

    print(f"总交易数: {len(records)}")

    # 统计大单
    large_trades = [r for r in records if float(r.get("q", 0)) >= 10]
    print(f"大单数量 (>=10 ETH): {len(large_trades)}")

    # 价格统计
    prices = [float(r.get("p", 0)) for r in records if r.get("p")]
    if prices:
        print(f"价格范围: ${min(prices):.2f} - ${max(prices):.2f}")
        print(f"平均价格: ${sum(prices)/len(prices):.2f}")

    # 交易量统计
    volumes = [float(r.get("q", 0)) for r in records if r.get("q")]
    if volumes:
        print(f"交易量范围: {min(volumes):.2f} - {max(volumes):.2f} ETH")
        print(f"平均交易量: {sum(volumes)/len(volumes):.2f} ETH")
        print(f"总交易量: {sum(volumes):.2f} ETH")

    # 买卖方向统计
    buy_count = sum(1 for r in records if not r.get("m", False))
    sell_count = sum(1 for r in records if r.get("m", False))
    print(f"买单数量: {buy_count}")
    print(f"卖单数量: {sell_count}")


def export_to_json(records, output_file):
    """将BSON数据导出为JSON文件"""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2, default=str)
        print(f"数据已导出到: {output_file}")
    except Exception as e:
        print(f"导出JSON时出错: {e}")


def main():
    parser = argparse.ArgumentParser(description="分析币安交易BSON数据")
    parser.add_argument("file", help="BSON文件路径")
    parser.add_argument("--export", help="导出为JSON文件")
    parser.add_argument("--sample", type=int, help="显示前N条记录")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"文件不存在: {args.file}")
        return

    print(f"正在分析文件: {args.file}")
    records = read_bson_file(args.file)

    if args.sample:
        print(f"\n前{args.sample}条记录:")
        for i, record in enumerate(records[: args.sample]):
            print(f"{i+1}. {record}")

    print(f"\n=== 分析结果 ===")
    analyze_trades(records)

    if args.export:
        export_to_json(records, args.export)


if __name__ == "__main__":
    main()
