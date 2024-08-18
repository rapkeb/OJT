from prometheus_client.core import GaugeMetricFamily


class LowStockPercentage:
    def __init__(self, low_stock_threshold=10):
        self.low_stock_threshold = low_stock_threshold
        self.total_items = 0
        self.low_stock_items = 0

    def update_inventory(self, inventory):
        """
        Update the count of total items and low stock items based on the provided inventory.

        :param inventory: List of inventory items where each item has a 'stock' attribute.
        """
        self.total_items = len(inventory.items)
        self.low_stock_items = sum(1 for item in inventory.items if item.amount < self.low_stock_threshold)

    def get_percentage(self):
        if self.total_items == 0:
            return 0.0
        return (self.low_stock_items / self.total_items) * 100

    def collect(self):
        metric = GaugeMetricFamily(
            'low_stock_percentage',
            'Percentage of inventory items that are low on stock'
        )
        metric.add_metric([], self.get_percentage())
        yield metric
