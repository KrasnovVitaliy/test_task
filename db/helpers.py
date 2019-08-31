from sqlalchemy import create_engine
import db.sessions as sessions
from db.assets import Assets
from db.assets_prices import AssetsPrices
from lib.singleton import Singleton
from sqlalchemy import desc

import config
import datetime

import logging

logger = logging.getLogger(__name__)


class DbHelpers(Singleton):
    """
    Class with help functions to work with DB
    """
    _session = sessions.get()
    _rates = {}
    _rates_list = []

    def get_assets(self):
        """
        Get assets map
        :return: Map<asset name>asset id
        """
        return self._rates

    def get_assets_list(self):
        """
        Get assets list
        :return: Rates list
        """
        return self._rates_list

    def load_assets(self):
        """
        Loading assets to memory. To avoid additional requests to DB.
        :return: None
        """
        results = self._session.query(Assets).all()
        for result in results:
            self._rates[result.name] = result.id
            self._rates_list.append({"id": result.id, "name": result.name})

    def calculate_data(self, rate_price):
        """
        Calculate value based on formula (ASK+BID)/2
        :param rate_price: Rate price value
        :return: Calculated value
        """
        return (float(rate_price["Ask"]) + float(rate_price["Bid"])) / 2

    def save_rates_prices(self, rates_prices, timestamp):
        """
        Saving rate prices to DB
        :param rates_prices: Rates prices list
        :param timestamp: Rate price request timestamp
        :return: None
        """

        logger.debug("Saving rate prices to DB")
        for rate_price in rates_prices:
            rate_id = self._rates[rate_price["Symbol"]]
            value = self.calculate_data(rate_price)

            self._session.add(AssetsPrices(rate=rate_id, value=value, timestamp=timestamp))
            self._session.commit()

    def get_init_prices(self, asset_id):
        """
        Get asset prices for configured interval(HISTORY_INTERVAL_SEC). This function call once when new user
        subscribe to asset
        :param asset_id: Asset id
        :return: rate prices list
        """

        logger.debug("Getting init prices for last {} seconds".format(config.HISTORY_INTERVAL_SEC))
        results = self._session.query(Assets, AssetsPrices) \
            .filter(AssetsPrices.rate == asset_id) \
            .filter(AssetsPrices.timestamp >= int(datetime.datetime.utcnow().timestamp()) - config.HISTORY_INTERVAL_SEC) \
            .order_by(desc(AssetsPrices.timestamp)) \
            .all()

        rates_prices = []
        for result in results:
            rates_prices.append(
                {
                    "assetName": result[0].name,
                    "assetId": result[0].id,
                    "time": result[1].timestamp,
                    "value": result[1].value,
                }
            )
        return rates_prices

    def delete_old_records(self, threshold_timestamp):
        logger.info("Delete old assets prices records with threshold timestamp: {}".format(threshold_timestamp))
        self._session.query(AssetsPrices).filter(
            AssetsPrices.timestamp < threshold_timestamp).delete()
        self._session.commit()


def prepare_db():
    """
    Function to prepare db and create all tables and start records
    :return: None
    """
    engine = create_engine(config.DB_URI)

    Assets.metadata.drop_all(engine)
    AssetsPrices.metadata.drop_all(engine)

    Assets.metadata.create_all(engine)
    AssetsPrices.metadata.create_all(engine)

    session = sessions.get()
    for item in config.SELECTED_ASSETS:
        rate = Assets(name=item)
        logger.debug("Creating {} record".format(item))
        session.add(rate)
        session.commit()


if __name__ == "__main__":
    prepare_db()
