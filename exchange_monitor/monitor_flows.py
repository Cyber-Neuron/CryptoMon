import logging
import time
from datetime import datetime
from typing import Optional

import psycopg2
import pytz
import schedule
from arkham import ArkhamClient
from db_utils import get_db_connection, get_or_create_chain, get_or_create_token
from psycopg2.extras import DictCursor

logger = logging.getLogger(__name__)


class FlowMonitor:
    def __init__(self):
        """Initialize the flow monitor."""
        self.client = ArkhamClient(use_proxy=True)
        self._init_db()

    def _init_db(self):
        """Initialize the database with required tables."""
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Create flows table
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS token_flows (
                id SERIAL PRIMARY KEY,
                token_id INTEGER NOT NULL REFERENCES tokens(id),
                chain_id INTEGER NOT NULL REFERENCES chains(id),
                timestamp INTEGER NOT NULL,
                inflow DECIMAL(20,6) NOT NULL,
                outflow DECIMAL(20,6) NOT NULL,
                inflow_count INTEGER NOT NULL,
                outflow_count INTEGER NOT NULL,
                net_flow DECIMAL(20,6) NOT NULL,
                inflow_usd DECIMAL(20,6) NOT NULL,
                outflow_usd DECIMAL(20,6) NOT NULL,
                net_flow_usd DECIMAL(20,6) NOT NULL,
                created_at INTEGER NOT NULL
            )
            """
            )

            # Create index on timestamp and token
            cursor.execute(
                """
            CREATE INDEX IF NOT EXISTS idx_token_flows_timestamp_token 
            ON token_flows(timestamp, token_id)
            """
            )

            conn.commit()
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def _store_flows(self, token: str, chain: str, stats: dict):
        """Store flow statistics in the database.

        Args:
            token: Token symbol
            chain: Chain name
            stats: Statistics dictionary from ArkhamClient
        """
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Get or create token and chain records
            chain_id = get_or_create_chain(cursor, chain)
            token_id = get_or_create_token(cursor, token, chain_id)

            if not token_id or not chain_id:
                logger.error(f"Failed to get/create token or chain records")
                return

            current_time = int(datetime.now(pytz.UTC).timestamp())

            for interval in stats["interval_stats"]:
                cursor.execute(
                    """
                INSERT INTO token_flows (
                    token_id, chain_id, timestamp, inflow, outflow, 
                    inflow_count, outflow_count, net_flow, 
                    inflow_usd, outflow_usd, net_flow_usd,
                    created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        token_id,
                        chain_id,
                        interval["timestamp"],
                        interval["inflow"],
                        interval["outflow"],
                        interval["inflow_count"],
                        interval["outflow_count"],
                        interval["inflow"] - interval["outflow"],
                        interval.get("inflow_usd", 0),
                        interval.get("outflow_usd", 0),
                        interval.get("inflow_usd", 0) - interval.get("outflow_usd", 0),
                        current_time,
                    ),
                )

            conn.commit()
        except Exception as e:
            logger.error(f"Error storing flows: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def monitor_flows(
        self, tokens="usd-coin, tether, ethereum", chains="ethereum", usd_gte=100000
    ):
        """Monitor token flows and store in database.

        Args:
            token: Token symbol to monitor
            chains: Comma-separated list of chains
            usd_gte: Minimum USD value to include
        """

        for token in tokens.split(","):
            token = token.strip()
            try:
                # Get flows for the last 10 minutes
                stats = self.client.get_token_flow_stats(
                    token=token,
                    time_last="10m",
                    interval_minutes=5,  # 10-minute intervals
                    chains=chains,
                    usd_gte=usd_gte,
                    store_to_db=True,
                )

                # Store flows in database
                self._store_flows(token, chains, stats)

                # Print current status
                print(
                    f"\n=== Flow Monitor Status ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ==="
                )
                print(f"Token: {token}")
                print(f"Total Inflow: {stats['total_inflow']:,.2f}")
                print(f"Total Outflow: {stats['total_outflow']:,.2f}")
                print(
                    f"Net Flow: {stats['total_inflow'] - stats['total_outflow']:,.2f}"
                )

            except Exception as e:
                logger.error(f"Error monitoring flows: {e}")

    def start_monitoring(self, tokens="usd-coin", chains="ethereum", usd_gte=100000):
        """Start the monitoring process.

        Args:
            token: Token symbol to monitor
            chains: Comma-separated list of chains
            usd_gte: Minimum USD value to include
        """
        print(f"Starting flow monitor for {tokens}...")
        print("Press Ctrl+C to stop")

        # Run immediately on start
        self.monitor_flows(tokens, chains, usd_gte)

        # Schedule to run every 5 minutes
        schedule.every(1).minutes.do(
            self.monitor_flows, tokens=tokens, chains=chains, usd_gte=usd_gte
        )

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping flow monitor...")


if __name__ == "__main__":
    # Create and start the monitor
    monitor = FlowMonitor()
    logging.basicConfig(level=logging.INFO)
    monitor.start_monitoring(
        tokens="ethereum,usd-coin,tether", chains="ethereum", usd_gte=10000
    )
