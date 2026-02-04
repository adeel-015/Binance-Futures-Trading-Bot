# Binance Futures Trading Bot

A Python CLI application for placing MARKET and LIMIT orders on Binance Futures Testnet with comprehensive logging, input validation, and error handling.

## Features

- **Order Types**: Support for both MARKET and LIMIT orders
- **CLI Interface**: Clean command-line interface using Click framework
- **Input Validation**: Comprehensive validation for all order parameters
- **Structured Logging**: Rotating file logs with DEBUG level detail
- **Error Handling**: Detailed error messages and logging for debugging
- **Testnet Ready**: Pre-configured for Binance Futures Testnet
- **Security**: API credentials loaded from environment variables

## Screenshots

### Limit Order
![LIMIT](https://github.com/adeel-015/Binance-Futures-Trading-Bot/blob/master/screenshots/Limit.png)

### Market Order
![MARKET](https://github.com/adeel-015/Binance-Futures-Trading-Bot/blob/master/screenshots/Market.png)

## Setup Steps

### 1. Clone or Setup Project

```bash
cd /Users/PATH_TO_REPO/trading_bot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**macOS/Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Credentials

Copy the environment template:

```bash
cp .env.example .env
```

Edit `.env` and add your Binance Futures Testnet credentials:

```
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_secret_key_here
BINANCE_TESTNET_URL=https://testnet.binancefuture.com
```

### 6. Verify Testnet Account

Create a testnet account at: https://testnet.binancefuture.com

- Register for Binance Futures Testnet
- Generate API key and secret
- Ensure sufficient testnet balance for testing

## How to Run

### Market Order Example

Place a market BUY order for 0.003 BTC:

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.003
```

### Limit Order Example

Place a limit SELL order for 0.01 ETH at 3500.50:

```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3500.50
```

### Get Help

```bash
python cli.py --help
```

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py              # Package initialization
│   ├── client.py                # Binance API client wrapper
│   ├── orders.py                # Order service layer
│   ├── validators.py            # Input validation functions
│   └── logging_config.py        # Logging configuration
├── logs/
│   ├── .gitkeep                 # Logs directory
│   └── trading_bot.log          # Generated log file
├── cli.py                       # CLI entry point
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

### Module Responsibilities

**`bot/client.py` - Binance Client Wrapper**

- Initializes connection to Binance Futures Testnet
- Tests API credentials connectivity
- Implements `place_market_order()` and `place_limit_order()` methods
- Handles Binance API exceptions with detailed logging

**`bot/orders.py` - Order Service Layer**

- Orchestrates order placement workflow
- Validates inputs using validators module
- Routes orders to appropriate client methods
- Formats and normalizes API responses
- Provides formatted logging of order details

**`bot/validators.py` - Input Validation**

- `validate_symbol()` - Ensures valid trading pair format
- `validate_side()` - Ensures BUY or SELL
- `validate_order_type()` - Ensures MARKET or LIMIT
- `validate_quantity()` - Ensures positive decimal quantity
- `validate_price()` - Ensures positive decimal price (required for LIMIT)
- `validate_all_inputs()` - Orchestrates all validations

**`bot/logging_config.py` - Logging Configuration**

- Configures Python logging with rotating file handler
- Log file: `logs/trading_bot.log` (5MB max, 5 backups)
- Console: INFO level, File: DEBUG level
- Provides `get_logger(name)` for module-specific loggers

**`cli.py` - CLI Entry Point**

- Click-based command-line interface
- Colored output for success/error states
- Orchestrates initialization → validation → order placement
- Proper exit codes (0 success, 1 failure)

## Configuration

Environment variables (in `.env`):

```
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_secret_key_here
BINANCE_TESTNET_URL=https://testnet.binancefuture.com
```

**File Logging Configuration** (`bot/logging_config.py`):

- Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- Log Level: DEBUG (captures all details)
- File Handler: RotatingFileHandler (5MB max, keeps 5 backups)
- Console Handler: INFO level

## API Details

### Binance Futures Testnet

- **Base URL**: https://testnet.binancefuture.com
- **API Documentation**: https://binance-docs.github.io/apidocs/futures/en
- **Order Types**: MARKET, LIMIT, STOP, TRAILING_STOP_MARKET, etc.
- **Time in Force**: GTC (Good-Till-Cancelled), IOC (Immediate or Cancel), FOK (Fill or Kill)

### Order Request Format

**Market Order:**

- Symbol: e.g., BTCUSDT, ETHUSDT
- Side: BUY or SELL
- Type: MARKET
- Quantity: Positive decimal number

**Limit Order:**

- Symbol: e.g., BTCUSDT, ETHUSDT
- Side: BUY or SELL
- Type: LIMIT
- Quantity: Positive decimal number
- Price: Positive decimal number (required)

## Assumptions

- **Python Version**: Python 3.8 or higher required
- **Account**: Active Binance Futures Testnet account
- **Balance**: Sufficient testnet balance for orders (USDT for margin)
- **Internet**: Stable internet connectivity for API access
- **API Keys**: Valid API key and secret from testnet account
- **Symbol Format**: Standard Binance format (e.g., BTCUSDT, not BTC/USDT)

## Troubleshooting

### Common Errors

**"Missing BINANCE_API_KEY or BINANCE_API_SECRET"**

- Ensure `.env` file exists in the project root
- Verify `BINANCE_API_KEY` and `BINANCE_API_SECRET` are set
- Check that no extra spaces around values in `.env`

**"Invalid symbol: BTCUSDT"**

- Common issue: Using wrong symbol format
- Must be uppercase (BOT handles this)
- Verify symbol exists on testnet (try BTCUSDT, ETHUSDT, etc.)

**"Insufficient balance" or "Margin is insufficient"**

- Testnet account needs USDT balance for orders
- Visit https://testnet.binancefuture.com and deposit testnet funds
- Free testnet tokens are often available

**"Connection refused"**

- Check internet connectivity
- Verify `BINANCE_TESTNET_URL` is correct
- Testnet may be temporarily unavailable

**"Invalid API key provided"**

- Regenerate API key in testnet account settings
- Ensure no extra spaces in `.env`
- Verify using correct testnet (not mainnet) keys

### Checking Logs

All detailed logs are written to `logs/trading_bot.log`:

```bash
# View last 20 lines
tail -20 logs/trading_bot.log

# Follow real-time logs
tail -f logs/trading_bot.log

# Search for errors
grep ERROR logs/trading_bot.log
```

### Testnet vs Mainnet

**Testnet:**

- No real funds required
- Used for testing and development
- API Base: https://testnet.binancefuture.com
- Free testnet tokens available

**Mainnet:**

- Real trading with real funds
- Should only use after thorough testing
- Different API keys required
- Will need to change `.env` configuration

## Example Workflow

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Test market order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# 3. Check logs
tail logs/trading_bot.log

# 4. Test limit order
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 3500

# 5. Verify orders in testnet account
# Visit https://testnet.binancefuture.com/en/futures/BTCUSDT

# 6. Deactivate virtual environment when done
deactivate
```

## Dependencies

- **python-binance** (>=1.0.19): Official Binance API Python client
- **click** (>=8.1.0): Command-line interface framework
- **python-dotenv** (>=1.0.0): Environment variable management
- **requests** (>=2.31.0): HTTP library for fallback/debugging

All dependencies are defined in `requirements.txt` for easy installation.

## Error Handling Strategy

### Validation Layer

- Raises `ValueError` for invalid inputs
- Specific error messages guide user corrections
- All validation errors logged before raising

### Client Layer

- Catches `BinanceAPIException` for API errors
- Catches `BinanceRequestException` for network errors
- Logs full stack trace at DEBUG level
- Re-raises with context

### Service Layer

- Validates before API call
- Catches and logs client exceptions
- Returns structured responses

### CLI Layer

- Catches all exceptions
- Displays user-friendly messages
- Logs full details to file
- Proper exit codes (0 success, 1 failure)

## Architecture

```
┌─────────┐
│   CLI   │ (cli.py)
└────┬────┘
     │
     ▼
┌──────────────────┐
│ OrderService     │ (bot/orders.py)
│ - validate       │
│ - place_order    │
└────┬─────────────┘
     │
     ├─────────────────────────┐
     │                         │
     ▼                         ▼
┌──────────────┐      ┌────────────────┐
│ Validators   │      │ BinanceClient  │
│ - symbol     │      │ - API wrapper  │
│ - side       │      │ - error handle │
│ - quantity   │      │ - logging      │
│ - price      │      └────────┬───────┘
└──────────────┘               │
                               ▼
                        ┌──────────────┐
                        │ Binance API  │
                        │ (Testnet)    │
                        └──────────────┘
```

## Security Notes

- API credentials stored in `.env` (never commit to version control)
- `.gitignore` excludes `.env` and `.env.local`
- Credentials loaded via `python-dotenv` at runtime
- Log files exclude sensitive information
- All API calls go through testnet endpoint

## Contributing

This is a personal trading bot project. For improvements:

1. Test thoroughly on testnet first
2. Add comprehensive logging for debugging
3. Update README with new features
4. Keep error messages user-friendly
5. Maintain modular structure

## License

Personal project - Use at your own risk.

## Support

For issues:

1. Check `logs/trading_bot.log` for detailed error information
2. Review error messages in console output
3. Verify `.env` configuration
4. Check Binance API documentation
5. Ensure testnet account has sufficient balance
