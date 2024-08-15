from prometheus_client.core import GaugeMetricFamily
from prometheus_client.registry import Collector
from prometheus_client.core import GaugeMetricFamily


class AmountBoughtCollector(Collector):
    def __init__(self):
        # Dictionary to track the total amount bought in each range
        self.amount_ranges = {
            '5To10': 0,
            '10To100': 0,
            '100To1000': 0,
            '1000Above': 0
        }

    def observe_amount(self, price, amount):
        # Update the count based on the amount ranges
        if price > 1000:
            self.amount_ranges['1000Above'] += amount
        elif price > 100:
            self.amount_ranges['100To1000'] += amount
        elif price > 10:
            self.amount_ranges['10To100'] += amount
        elif price > 5:
            self.amount_ranges['5To10'] += amount

    def collect(self):
        for range_label, total_amount in self.amount_ranges.items():
            metric = GaugeMetricFamily(
                f'price_bought_above_{range_label}',
                f'Total amount of items bought above the price {range_label.replace("_", "to")}',
                value=total_amount
            )
            yield metric
