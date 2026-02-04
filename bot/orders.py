"""Order service for trading bot."""

from bot.logging_config import get_logger
from bot.validators import validate_all_inputs

logger = get_logger(__name__)


class OrderService:
    """Service layer for order placement."""

    def __init__(self, binance_client):
        """
        Initialize order service with a Binance client.

        Args:
            binance_client: BinanceClient instance
        """
        self.client = binance_client
        logger.info("OrderService initialized")

    def place_order(self, symbol, side, order_type, quantity, price=None):
        """
        Place an order with validation and error handling.

        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Order price (required for LIMIT, optional for MARKET)

        Returns:
            dict: Standardized order response with keys:
                  orderId, symbol, side, type, status, executedQty, avgPrice, timestamp

        Raises:
            ValueError: If validation fails
            BinanceAPIException: If API call fails
            BinanceRequestException: If network error occurs
        """
        try:
            # Validate all inputs
            validated = validate_all_inputs(symbol, side, order_type, quantity, price)

            # Log order request summary
            summary = format_order_summary(validated)
            logger.info(f"Order request: {summary}")

            # Place order through client
            if validated['order_type'] == 'MARKET':
                response = self.client.place_market_order(
                    validated['symbol'],
                    validated['side'],
                    validated['quantity']
                )
            else:  # LIMIT
                response = self.client.place_limit_order(
                    validated['symbol'],
                    validated['side'],
                    validated['quantity'],
                    validated['price']
                )

            # Extract and normalize response
            order_details = extract_order_details(response)

            # Log formatted response
            response_summary = format_order_response(order_details)
            logger.info(f"Order response: {response_summary}")

            return order_details

        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Order placement failed: {str(e)}")
            raise


def format_order_summary(order_params):
    """
    Format order parameters for logging.

    Args:
        order_params: Dictionary with order parameters

    Returns:
        str: Formatted order summary
    """
    summary = (
        f"Symbol={order_params['symbol']}, "
        f"Side={order_params['side']}, "
        f"Type={order_params['order_type']}, "
        f"Quantity={order_params['quantity']}"
    )

    if order_params.get('price') is not None:
        summary += f", Price={order_params['price']}"

    return summary


def format_order_response(order_details):
    """
    Format order response for logging.

    Args:
        order_details: Dictionary with order details

    Returns:
        str: Formatted order response
    """
    return (
        f"OrderID={order_details.get('orderId')}, "
        f"Symbol={order_details.get('symbol')}, "
        f"Side={order_details.get('side')}, "
        f"Type={order_details.get('type')}, "
        f"Status={order_details.get('status')}, "
        f"ExecutedQty={order_details.get('executedQty')}, "
        f"AvgPrice={order_details.get('avgPrice')}, "
        f"Timestamp={order_details.get('timestamp')}"
    )


def extract_order_details(response):
    """
    Extract and normalize order details from API response.

    Args:
        response: Order response from Binance API

    Returns:
        dict: Standardized order details
    """
    return {
        'orderId': response.get('orderId'),
        'symbol': response.get('symbol'),
        'side': response.get('side'),
        'type': response.get('type'),
        'status': response.get('status'),
        'executedQty': response.get('executedQty'),
        'avgPrice': response.get('avgPrice'),
        'timestamp': response.get('updateTime'),
    }
