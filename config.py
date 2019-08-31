import logging

# Service listening port
PORT = 8080
# Available connection hosts
HOST = '0.0.0.0'
# Rates HTTP server URL
RATES_URL = 'https://ratesjson.fxcm.com/DataDisplayer'

# Logging format
LOG_FORMAT = '%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s'
# Logging level
LOG_LEVEL = logging.DEBUG
# Logging file
LOG_FILE = None

# DB connection URI
DB_URI = 'sqlite:///./data.db'

# Processing assets list
SELECTED_ASSETS = ['EURUSD', 'USDJPY', 'GBPUSD', 'AUDUSD', 'USDCAD']

# Time interval for records returned to new subscribed user
HISTORY_INTERVAL_SEC = 1800  # 30 minutes in seconds

# Is need to delete old records older than history interval
DEELTE_OLD_RECORDS = True

# Delete old records every 1 min
DEELTE_OLD_RECORDS_INTERVAL_SEC = 60
