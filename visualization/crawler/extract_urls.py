import json
from typing import List, Tuple
from urllib.parse import urlparse

import fire


def convert_tron_url(url: str) -> str:
    """将 tron:TXID 格式转换为 tronscan URL"""
    if url.startswith("tron:"):
        txid = url[5:]  # 去掉 'tron:' 前缀
        return f"https://tronscan.org/#/transaction/{txid}"
    return url


def extract_urls_from_json(file_path: str) -> List[Tuple[str, str]]:
    """从单个 JSON 文件中提取 URL 和域名"""
    # 读取 JSON 文件
    with open(file_path, "r") as f:
        data = json.load(f)

    # 存储所有 URL 和域名
    urls_and_domains = []

    # 遍历数据
    for item in data:
        for transaction in item["list"]:
            # 解析 remark 字段中的 JSON 字符串
            remark = json.loads(transaction["remark"])
            # 提取 web URL
            if "web" in remark:
                url = remark["web"]
                # 转换 tron URL
                url = convert_tron_url(url)
                # 解析 URL 获取域名
                if url.startswith("https://tronscan.org"):
                    domain = "tronscan.org"
                else:
                    parsed_url = urlparse(url)
                    domain = parsed_url.netloc
                urls_and_domains.append((url, domain))

    return urls_and_domains


def extract_urls(*file_paths):
    """从多个 JSON 文件中提取 URL 和域名

    Args:
        *file_paths: 要处理的 JSON 文件路径列表
    """
    all_urls_and_domains = []

    for file_path in file_paths:
        try:
            # 提取 URL 和域名
            urls_and_domains = extract_urls_from_json(file_path)
            all_urls_and_domains.extend(urls_and_domains)
            print(f"从 {file_path} 中提取了 {len(urls_and_domains)} 个 URL")
        except FileNotFoundError:
            print(f"错误：找不到文件 {file_path}")
        except json.JSONDecodeError:
            print(f"错误：{file_path} 文件格式不正确")
        except Exception as e:
            print(f"处理 {file_path} 时发生错误：{str(e)}")

    if not all_urls_and_domains:
        print("没有找到任何 URL")
        return

    # 统计域名
    domain_counts = {}
    for _, domain in all_urls_and_domains:
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
    sample_urls = {}
    urls = []
    # 将 URL 和唯一域名分别写入文件
    with open("urls.txt", "w") as url_file, open("domain.txt", "w") as domain_file:
        # 写入 URL
        url_file.write("URL 列表：\n")
        for i, (url, _) in enumerate(all_urls_and_domains, 1):
            url_file.write(f"{i}. {url}\n")
            urls.append(url)
        # 写入唯一域名
        unique_domains = sorted(domain_counts.keys())
        for domain in unique_domains:
            domain_file.write(f"{domain}\n")
    # print(unique_domains, urls)
    for domain in unique_domains:
        if "tron" in domain:
            domain = "tron"
        for url in urls:
            # print(domain, url)
            if domain in url:
                sample_urls[domain] = url
    print(sample_urls)
    # 控制台输出统计信息
    print("\n域名统计：")
    for domain, count in domain_counts.items():
        print(f"{domain}: {count} 个 URL")

    print(f"\n数据已保存到 urls.txt 和 domain.txt")
    print(f"总共找到 {len(all_urls_and_domains)} 个 URL")


if __name__ == "__main__":
    fire.Fire()
