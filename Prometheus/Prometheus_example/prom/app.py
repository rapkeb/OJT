from fastapi import FastAPI, Depends
import uvicorn
from .main.routers.items import router as items_router
from .main.routers.metrics import router as metrics_router
from .main.utils.inventory_helper import get_inventory


app = FastAPI()


# Include routes and inject the Inventory instance
app.include_router(items_router, dependencies=[Depends(get_inventory)])
app.include_router(metrics_router)


if __name__ == "__main__":
    # Start the FastAPI application on port 5001
    uvicorn.run(app, port=5001)
