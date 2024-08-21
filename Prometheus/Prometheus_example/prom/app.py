from fastapi import FastAPI, Depends
import uvicorn
from opentelemetry.sdk.resources import Resource

from .main.routers.items import router as items_router
from .main.routers.metrics import router as metrics_router
from .main.utils.inventory_helper import get_inventory

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()


# Include routes and inject the Inventory instance
app.include_router(items_router, dependencies=[Depends(get_inventory)])
app.include_router(metrics_router)

# Set up OpenTelemetry tracing with a service name
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({"service.name": "my_fastapi_service"})
    )
)
tracer = trace.get_tracer(__name__)

# Configure the OTLP exporter to send traces to Tempo
otlp_exporter = OTLPSpanExporter(endpoint="http://tempo:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app)


if __name__ == "__main__":
    # Start the FastAPI application on port 5001
    uvicorn.run(app, port=5001)
