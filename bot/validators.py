"""Input validation for trading bot."""

import re
from bot.logging_config import get_logger

logger = get_logger(__name__)


def validate_symbol(symbol):
    """
    Validate and normalize trading symbol.

    Args:
        symbol: Trading pair symbol (e.g., BTCUSDT)

    Returns:
        str: Uppercase symbol

    Raises:
        ValueError: If symbol is invalid
    """
    if not symbol or not isinstance(symbol, str):
        logger.warning(f"Invalid symbol type: {type(symbol)}")
        raise ValueError("Symbol must be a non-empty string")

    symbol = symbol.upper().strip()

    # Check if symbol is alphanumeric
    if not re.match(r'^[A-Z0-9]+$', symbol):
        logger.warning(f"Invalid symbol format: {symbol}")
        raise ValueError(f"Symbol must contain only alphanumeric characters, got: {symbol}")

    if len(symbol) < 2:
        logger.warning(f"Symbol too short: {symbol}")
        raise ValueError(f"Symbol must be at least 2 characters, got: {len(symbol)}")

    logger.debug(f"Symbol validated: {symbol}")
    return symbol


def validate_side(side):
    """
    Validate order side (BUY or SELL).

    Args:
        side: Order side

    Returns:
        str: Uppercase side (BUY or SELL)

    Raises:
        ValueError: If side is invalid
    """
    if not side or not isinstance(side, str):
        logger.warning(f"Invalid side type: {type(side)}")
        raise ValueError("Side must be a non-empty string")

    side = side.upper().strip()

    if side not in ('BUY', 'SELL'):
        logger.warning(f"Invalid side value: {side}")
        raise ValueError(f"Side must be 'BUY' or 'SELL', got: {side}")

    logger.debug(f"Side validated: {side}")
    return side


def validate_order_type(order_type):
    """
    Validate order type (MARKET or LIMIT).

    Args:
        order_type: Order type

    Returns:
        str: Uppercase order type (MARKET or LIMIT)

    Raises:
        ValueError: If order type is invalid
    """
    if not order_type or not isinstance(order_type, str):
        logger.warning(f"Invalid order_type type: {type(order_type)}")
        raise ValueError("Order type must be a non-empty string")

    order_type = order_type.upper().strip()

    if order_type not in ('MARKET', 'LIMIT'):
        logger.warning(f"Invalid order_type value: {order_type}")
        raise ValueError(f"Order type must be 'MARKET' or 'LIMIT', got: {order_type}")

    logger.debug(f"Order type validated: {order_type}")
    return order_type


def validate_quantity(quantity):
    """
    Validate order quantity as positive decimal number.

    Args:
        quantity: Order quantity (str or float)

    Returns:
        float: Validated quantity

    Raises:
        ValueError: If quantity is invalid
    """
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        logger.warning(f"Invalid quantity format: {quantity}")
        raise ValueError(f"Quantity must be a valid number, got: {quantity}")

    if qty <= 0:
        logger.warning(f"Invalid quantity value: {qty}")
        raise ValueError(f"Quantity must be positive, got: {qty}")

    logger.debug(f"Quantity validated: {qty}")
    return qty


def validate_price(price, order_type):
    """
    Validate order price (required for LIMIT orders, positive decimal).

    Args:
        price: Order price (str, float, or None)
        order_type: Order type (MARKET or LIMIT)

    Returns:
        float or None: Validated price (None for MARKET orders)

    Raises:
        ValueError: If price is invalid or required for LIMIT but missing
    """
    if order_type == 'LIMIT':
        if price is None:
            logger.warning("Price is required for LIMIT orders")
            raise ValueError("Price is required for LIMIT orders")

        try:
            px = float(price)
        except (TypeError, ValueError):
            logger.warning(f"Invalid price format: {price}")
            raise ValueError(f"Price must be a valid number, got: {price}")

        if px <= 0:
            logger.warning(f"Invalid price value: {px}")
            raise ValueError(f"Price must be positive, got: {px}")

        logger.debug(f"Price validated: {px}")
        return px
    else:  # MARKET order
        if price is not None:
            logger.warning(f"Price not required for MARKET orders, ignoring: {price}")
        return None


def validate_all_inputs(symbol, side, order_type, quantity, price=None):
    """
    Validate all inputs together.

    Args:
        symbol: Trading pair symbol
        side: Order side (BUY or SELL)
        order_type: Order type (MARKET or LIMIT)
        quantity: Order quantity
        price: Order price (optional, required for LIMIT)

    Returns:
        dict: Dictionary with validated and normalized values

    Raises:
        ValueError: If any input is invalid
    """
    logger.info(f"Validating inputs - Symbol: {symbol}, Side: {side}, Type: {order_type}, Qty: {quantity}, Price: {price}")

    try:
        validated = {
            'symbol': validate_symbol(symbol),
            'side': validate_side(side),
            'order_type': validate_order_type(order_type),
            'quantity': validate_quantity(quantity),
        }

        validated['price'] = validate_price(price, validated['order_type'])

        logger.info("All inputs validated successfully")
        return validated

    except ValueError as e:
        logger.error(f"Validation failed: {str(e)}")
        raise
