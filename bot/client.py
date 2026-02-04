"""Binance Futures API client wrapper."""

import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv

from bot.logging_config import get_logger

logger = get_logger(__name__)


class BinanceClient:
    """Wrapper for Binance Futures API client with testnet support."""

    def __init__(self):
        """
        Initialize Binance client with credentials from environment variables.

        Raises:
            ValueError: If API credentials are missing
            BinanceRequestException: If connection test fails
        """
        load_dotenv()

        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        self.testnet_url = os.getenv(
            'BINANCE_TESTNET_URL',
            'https://testnet.binancefuture.com'
        )

        if not self.api_key or not self.api_secret:
            logger.error("Missing BINANCE_API_KEY or BINANCE_API_SECRET in environment")
            raise ValueError(
                "API credentials not found. Please set BINANCE_API_KEY and "
                "BINANCE_API_SECRET in .env file"
            )

        logger.debug("Initializing Binance client for testnet")

        # Initialize client with testnet
        self.client = Client(
            api_key=self.api_key,
            api_secret=self.api_secret,
            testnet=True
        )

        # Override base URLs for testnet
        self.client.API_URL = f"{self.testnet_url}/api"
        self.client.API_TESTNET_URL = f"{self.testnet_url}/api"

        # Test connection
        self.test_connection()

    def test_connection(self):
        """
        Test connection to Binance API and verify credentials.

        Raises:
            BinanceAPIException: If API credentials are invalid
            BinanceRequestException: If connection fails
        """
        try:
            logger.info("Testing connection to Binance Futures Testnet")
            # Use authenticated call to verify API credentials
            account = self.client.futures_account()
            logger.info("Successfully connected to Binance Futures Testnet and verified API credentials")
            return True
        except BinanceAPIException as e:
            logger.error(f"API error during connection test: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Connection error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during connection test: {str(e)}")
            raise

    def get_futures_client(self):
        """
        Get the underlying futures client instance.

        Returns:
            binance.Client: Configured client for futures trading
        """
        return self.client

    def place_market_order(self, symbol, side, quantity):
        """
        Place a market order on Binance Futures.

        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            quantity: Order quantity

        Returns:
            dict: Order response from API

        Raises:
            BinanceAPIException: If API call fails
            BinanceRequestException: If network error occurs
        """
        try:
            logger.info(f"Placing MARKET order - Symbol: {symbol}, Side: {side}, Qty: {quantity}")

            # Place market order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )

            logger.info(f"Market order placed successfully. Order ID: {order.get('orderId')}")
            logger.debug(f"Order response: {order}")

            return order

        except BinanceAPIException as e:
            logger.error(f"API error placing market order: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Network error placing market order: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing market order: {str(e)}")
            raise

    def place_limit_order(self, symbol, side, quantity, price):
        """
        Place a limit order on Binance Futures.

        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            quantity: Order quantity
            price: Order price

        Returns:
            dict: Order response from API

        Raises:
            BinanceAPIException: If API call fails
            BinanceRequestException: If network error occurs
        """
        try:
            logger.info(
                f"Placing LIMIT order - Symbol: {symbol}, Side: {side}, "
                f"Qty: {quantity}, Price: {price}"
            )

            # Place limit order
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                timeInForce='GTC',  # Good-Till-Cancelled
                quantity=quantity,
                price=price
            )

            logger.info(f"Limit order placed successfully. Order ID: {order.get('orderId')}")
            logger.debug(f"Order response: {order}")

            return order

        except BinanceAPIException as e:
            logger.error(f"API error placing limit order: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Network error placing limit order: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing limit order: {str(e)}")
            raise
