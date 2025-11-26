"""Tor network management and configuration."""

import os
import socket

import requests
import socks
from core.constants import PROXY_HOST, PROXY_PORT, TOR_PROXY
from utils.logging_utils import setup_logging

logger = setup_logging()


def configure_tor():
    """Configure system to use Tor network."""
    # Configure socket to use Tor
    socks.set_default_proxy(socks.SOCKS5, PROXY_HOST, PROXY_PORT)
    socket.socket = socks.socksocket

    # Configure requests to use Tor
    proxies = {"http": TOR_PROXY, "https": TOR_PROXY}
    return proxies


def create_tor_socket() -> socks.socksocket:
    """Create a new socket configured to use Tor."""
    sock = socks.socksocket()
    sock.set_proxy(
        proxy_type=socks.SOCKS5,
        addr=PROXY_HOST,
        port=PROXY_PORT,
        rdns=True,  # Enable remote DNS resolution through Tor
    )
    return sock


def test_tor_connection() -> bool:
    """Test if Tor connection is working properly."""
    logger.info("Testing Tor connection...")
    try:
        # Test 1: Check if we can reach check.torproject.org
        response = requests.get(
            "https://check.torproject.org/api/ip",
            proxies={"http": TOR_PROXY, "https": TOR_PROXY},
            timeout=10,
        )
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Tor IP: {data.get('IP')}")
            logger.info(f"Tor exit node: {data.get('ExitNode')}")
            logger.info("Tor connection test successful!")
            return True
        else:
            logger.error(f"Tor test failed with status code: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Tor connection test failed: {e}")
        return False
