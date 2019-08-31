import logging

PORT = 8080
HOST = '0.0.0.0'
RATES_URL = 'https://ratesjson.fxcm.com/DataDisplayer'

# Logging
LOG_FORMAT = '%(asctime)-15s | %(levelname)s | %(filename)s | %(lineno)d: %(message)s'
LOG_LEVEL = logging.DEBUG
LOG_FILE = None

# DB
DB_URI = 'sqlite:///./data.db'

SELECTED_ASSETS = ['EURUSD', 'USDJPY', 'GBPUSD', 'AUDUSD', 'USDCAD']
HISTORY_INTERVAL_SEC = 10
