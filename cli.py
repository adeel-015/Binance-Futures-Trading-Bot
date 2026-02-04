"""CLI interface for trading bot."""

import sys
import click

from bot.logging_config import get_logger
from bot.client import BinanceClient
from bot.orders import OrderService

logger = get_logger(__name__)


@click.command()
@click.option(
    '--symbol',
    required=True,
    help='Trading pair (e.g., BTCUSDT)'
)
@click.option(
    '--side',
    required=True,
    type=click.Choice(['BUY', 'SELL'], case_sensitive=False),
    help='Order side: BUY or SELL'
)
@click.option(
    '--type',
    'order_type',
    required=True,
    type=click.Choice(['MARKET', 'LIMIT'], case_sensitive=False),
    help='Order type: MARKET or LIMIT'
)
@click.option(
    '--quantity',
    required=True,
    type=float,
    help='Order quantity'
)
@click.option(
    '--price',
    type=float,
    default=None,
    help='Price (required for LIMIT orders)'
)
def main(symbol, side, order_type, quantity, price):
    """
    Place an order on Binance Futures Testnet.

    Examples:

    Market order:
    \b
    python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

    Limit order:
    \b
    python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3500.50
    """
    try:
        # Initialize logging
        click.echo(click.style("=" * 60, fg='cyan'))
        click.echo(click.style("ORDER REQUEST", fg='cyan', bold=True))
        click.echo(click.style("=" * 60, fg='cyan'))

        # Display request parameters
        click.echo(f"Symbol:   {symbol}")
        click.echo(f"Side:     {side}")
        click.echo(f"Type:     {order_type}")
        click.echo(f"Quantity: {quantity}")
        if price is not None:
            click.echo(f"Price:    {price}")
        click.echo()

        logger.info("=" * 60)
        logger.info("CLI order placement initiated")
        logger.info(f"Symbol: {symbol}, Side: {side}, Type: {order_type}, Qty: {quantity}, Price: {price}")

        # Initialize Binance client
        click.echo(click.style("Connecting to Binance Futures Testnet...", fg='yellow'))
        client = BinanceClient()
        click.echo(click.style("✓ Connected to Binance Futures Testnet", fg='green'))
        click.echo()

        # Initialize order service
        service = OrderService(client)

        # Place order
        click.echo(click.style("Placing order...", fg='yellow'))
        response = service.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )

        # Display response
        click.echo()
        click.echo(click.style("=" * 60, fg='cyan'))
        click.echo(click.style("ORDER RESPONSE", fg='cyan', bold=True))
        click.echo(click.style("=" * 60, fg='cyan'))

        click.echo(f"Order ID:       {response.get('orderId')}")
        click.echo(f"Symbol:         {response.get('symbol')}")
        click.echo(f"Side:           {response.get('side')}")
        click.echo(f"Type:           {response.get('type')}")
        click.echo(f"Status:         {response.get('status')}")
        click.echo(f"Executed Qty:   {response.get('executedQty')}")
        click.echo(f"Avg Price:      {response.get('avgPrice')}")
        click.echo(f"Timestamp:      {response.get('timestamp')}")
        click.echo()

        # Display result
        click.echo(click.style("=" * 60, fg='cyan'))
        click.echo(click.style("RESULT", fg='cyan', bold=True))
        click.echo(click.style("=" * 60, fg='cyan'))
        click.echo(click.style("✓ Order placed successfully!", fg='green', bold=True))
        click.echo()

        logger.info("Order placement completed successfully")
        sys.exit(0)

    except ValueError as e:
        # Validation errors
        click.echo()
        click.echo(click.style("=" * 60, fg='red'))
        click.echo(click.style("VALIDATION ERROR", fg='red', bold=True))
        click.echo(click.style("=" * 60, fg='red'))
        click.echo(click.style(f"✗ {str(e)}", fg='red'))
        click.echo()

        logger.error(f"Validation error: {str(e)}")
        sys.exit(1)

    except Exception as e:
        # API or network errors
        error_message = str(e)

        # Extract useful error info from Binance exceptions if available
        if hasattr(e, 'message'):
            error_message = e.message
        elif hasattr(e, 'status_code'):
            error_message = f"API Error {e.status_code}: {str(e)}"

        click.echo()
        click.echo(click.style("=" * 60, fg='red'))
        click.echo(click.style("ERROR", fg='red', bold=True))
        click.echo(click.style("=" * 60, fg='red'))
        click.echo(click.style(f"✗ {error_message}", fg='red'))
        click.echo()
        click.echo(click.style("Check logs/trading_bot.log for details", fg='yellow'))
        click.echo()

        logger.error(f"Order placement failed: {error_message}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
