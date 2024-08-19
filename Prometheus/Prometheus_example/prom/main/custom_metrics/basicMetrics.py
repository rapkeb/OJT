from prometheus_client import Summary, Counter, Histogram, REGISTRY

from prom.main.custom_metrics.amountBoughtSummary import AmountBoughtCollector
from prom.main.custom_metrics.lowStockPercent import LowStockPercentage
from prom.main.custom_metrics.purchaseSuccessRatio import PurchaseSuccessRatio

# Define labels for the request_latency Summary
request_latency = Summary(
    'request_latency_seconds',
    'Request latency in seconds',
    labelnames=['method']  # Define the labels
)

# Define labels for the requests_total Counter
requests_total = Counter(
    'requests_total',
    'Total number of requests',
    labelnames=['method']  # Define the labels
)

# Define labels for request duration Histogram
request_duration = Histogram(
    'request_duration_seconds',
    'Histogram of request durations in seconds',
    labelnames=['method'],  # Define the labels
    buckets=[0.1, 0.5, 1, 2, 5, 10]  # Define histogram buckets
)

DB_OPERATION_DURATION = Histogram('db_operation_duration_seconds', 'Time taken for database operations')


# Custom metric instance
purchase_success_ratio = PurchaseSuccessRatio()
low_stock_metric = LowStockPercentage(low_stock_threshold=10)
amount_bought_summary = AmountBoughtCollector()
REGISTRY.register(purchase_success_ratio)
REGISTRY.register(amount_bought_summary)
REGISTRY.register(low_stock_metric)
