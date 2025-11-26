import psycopg2
from psycopg2.extras import execute_values

# 文件路径
FILE_PATH = "hot2_wallets.txt"

# 数据库连接配置
import os
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/walletmonitor")
# Parse DATABASE_URL or use individual env vars
conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    dbname=os.getenv("DB_NAME", "walletmonitor"),
    user=os.getenv("DB_USER", "user"),
    password=os.getenv("DB_PASSWORD", "password"),
    port=int(os.getenv("DB_PORT", "5432")),
)


def parse_wallet_file(file_path):
    data = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) != 6:
                continue  # skip malformed line
            address = parts[0].lower()
            chain_id = int(parts[1])
            friendly_name = parts[2].strip()
            grp_type = parts[3].strip()
            grp_name = parts[4].strip()
            wallet_type_id = int(parts[5])
            data.append(
                (address, chain_id, friendly_name, grp_type, grp_name, wallet_type_id)
            )
    return data


def insert_wallets(data):
    with conn, conn.cursor() as cur:
        insert_sql = """
        INSERT INTO wallets (address, chain_id, friendly_name, grp_type, grp_name, wallet_type_id)
        VALUES %s
        ON CONFLICT (address, chain_id) DO NOTHING
        """
        execute_values(cur, insert_sql, data)
        print(f"Inserted {len(data)} rows (duplicates ignored).")


if __name__ == "__main__":
    wallets = parse_wallet_file(FILE_PATH)
    insert_wallets(wallets)
    conn.close()
