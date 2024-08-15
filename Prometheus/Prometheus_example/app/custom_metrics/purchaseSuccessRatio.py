from prometheus_client.core import GaugeMetricFamily


class PurchaseSuccessRatio:
    def __init__(self):
        self.total_purchase_attempts = 0
        self.successful_purchases = 0

    def increment_attempts(self):
        self.total_purchase_attempts += 1

    def increment_successes(self):
        self.successful_purchases += 1

    def get_ratio(self):
        if self.total_purchase_attempts == 0:
            return 0.0
        return self.successful_purchases / self.total_purchase_attempts

    def collect(self):
        metric = GaugeMetricFamily(
            'purchase_success_ratio',
            'Ratio of successful purchases to total purchase attempts'
        )
        metric.add_metric([], self.get_ratio())
        yield metric
