import aiohttp
import config
import demjson
import logging

logger = logging.getLogger(__name__)


def clear_response(rsp):
    """
    Cleare response body to make it suitable for demjson lib
    :param rsp: response body string
    :return: Cleared response body
    """
    return rsp.replace("null(", "").replace(");", "")


async def fetch(session, url):
    """
    Send request to HTTP server
    :param session: aiohttp ClientSession
    :param url: requested url
    :return: String response body
    """
    async with session.get(url) as response:
        rsp_body = await response.text()
        logger.debug("Received response body: {}".format(rsp_body))
        return clear_response(rsp_body)


async def get():
    """
    Get rates price from HTTP server
    :return: Rates list List<Map>
    """
    async with aiohttp.ClientSession() as session:
        rsp_body = await fetch(session, config.RATES_URL)
        rates = demjson.decode(rsp_body)
        logger.debug("Decoded rates response body: {}".format(rates))
        filtered_rates = list(filter(lambda rate: rate['Symbol'] in config.SELECTED_ASSETS, rates['Rates']))
        logger.debug("Filtered rates: {}".format(filtered_rates))

    return filtered_rates
