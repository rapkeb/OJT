from abc import ABC, abstractmethod
from prometheus_client import Counter, start_http_server, REGISTRY, generate_latest
from fastapi import FastAPI, Request, Response
from typing import Any
from functools import wraps


# Step 1: Create an Abstract Base Class for Prometheus Metrics
class PrometheusMetricsBase(ABC):
    def __init__(self, app: FastAPI, metrics_port: int = 8001):
        self.app = app
        self.metrics_port = metrics_port
        self.initialize_metrics()
        self.setup_routes(app)
        self.start_server()
        self.add_request_metrics(app)

    @abstractmethod
    def initialize_metrics(self):
        """Initialize Prometheus metrics"""
        pass

    @abstractmethod
    def before_request(self, request: Request):
        """Actions to take before a request"""
        pass

    @abstractmethod
    def after_request(self, request: Request, response: Response):
        """Actions to take after a request"""
        pass

    def setup_routes(self, app: FastAPI):
        """Setup Prometheus metrics route"""
        @app.get("/metrics")
        def metrics_route():
            metrics_data = generate_latest()
            return Response(content=metrics_data, media_type="text/plain")

    def start_server(self):
        """Start Prometheus metrics server"""
        start_http_server(self.metrics_port)

    def add_request_metrics(self, app: FastAPI):
        """Add middleware for request metrics"""
        @app.middleware("http")
        async def add_metrics_middleware(request: Request, call_next):
            response = await call_next(request)
            self.status_codes.labels(status_code=response.status_code).inc()
            return response


# Step 2: Create a Concrete Class for Request Counting
class StatusCodeCounterMetrics(PrometheusMetricsBase):
    def __init__(self, app: FastAPI):
        super().__init__(app)

    def initialize_metrics(self):
        self.status_codes = Counter('http_response_status_codes', 'Count of HTTP status codes', ['status_code'])

    def before_request(self, request: Request):
        pass  # Logic before processing a request (if needed)

    def after_request(self, request: Request, response: Response):
        pass

    def metric_decorator(self, func: Any):
        """Decorator to track metrics for a specific route"""
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        return wrapper


# Step 3: Initialize FastAPI App and Use Metrics
app = FastAPI()
# Instantiate the request counter metrics class
metrics = StatusCodeCounterMetrics(app)


# Example route with the metrics decorator applied
@app.get("/example")
@metrics.metric_decorator
async def example_route():
    return {"message": "Hello, world!"}

