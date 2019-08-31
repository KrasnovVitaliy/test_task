from lib.singleton import Singleton


class SubscriptionsDB(Singleton):
    """
    In memory db subscription db.
    """
    _connection_asset_relation = {}

    def get_subscriptions(self):
        """
        Get subscribers map
        :return: Map<subscriber socket>Asset id
        """
        return self._connection_asset_relation

    def set_subscription(self, connection, asset_id):
        """
        Add new subscriber
        :param connection: subscriber socket
        :param asset_id: Asset id
        :return: None
        """
        self._connection_asset_relation[connection] = asset_id

    def delete_subscription(self, connection):
        """
        Removing subscriber from DB
        :param connection: subscriber socket
        :return: None
        """
        del self._connection_asset_relation[connection]
