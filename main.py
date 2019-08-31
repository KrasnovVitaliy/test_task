import logging
import config
from ws.ws_server import WebsocketServer

# Configuring logger
logging.basicConfig(filename=config.LOG_FILE, filemode='w', level=config.LOG_LEVEL, format=config.LOG_FORMAT)
logger = logging.getLogger(__name__)


# Entry poiunt
def main():
    logger.info("Program started")
    WebsocketServer().run()


if __name__ == '__main__':
    main()
