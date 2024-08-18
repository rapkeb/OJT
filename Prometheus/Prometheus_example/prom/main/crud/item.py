import time
from fastapi import HTTPException
from prom.main.custom_metrics.basicMetrics import requests_total, request_duration, request_latency, amount_bought_summary, \
    low_stock_metric
from prom.main.custom_metrics.basicMetrics import purchase_success_ratio
from prom.main.schemas.inventory import Inventory
from prom.main.schemas.item import Item
from prom.main.utils.functions import save_inventory_to_env


async def root1(inventory: Inventory):
    method = 'get'  # Define the label value for GET request
    # Increment the total request count with the method label
    requests_total.labels(method=method).inc()
    start_time = time.time()
    # Simulate some work
    items = inventory.items
    # Measure request latency
    latency = time.time() - start_time
    request_latency.labels(method=method).observe(latency)
    request_duration.labels(method=method).observe(latency)
    low_stock_metric.update_inventory(inventory)
    return items


async def add_item1(item: Item, inventory: Inventory):
    method = 'post'  # Define the label value for POST request
    # Increment the total request count with the method label
    requests_total.labels(method=method).inc()
    start_time = time.time()
    for existing_item in inventory.items:
        if existing_item.name == item.name:
            existing_item.amount += item.amount
            save_inventory_to_env(inventory)
            latency = time.time() - start_time
            request_latency.labels(method=method).observe(latency)
            request_duration.labels(method=method).observe(latency)
            low_stock_metric.update_inventory(inventory)
            return {"message": f"Item '{item.name}' quantity updated to {existing_item.amount}"}

    inventory.items.append(item)
    save_inventory_to_env(inventory)
    latency = time.time() - start_time
    request_latency.labels(method=method).observe(latency)
    request_duration.labels(method=method).observe(latency)
    low_stock_metric.update_inventory(inventory)
    return {"message": "Item added successfully", "item": item}


async def buy_item1(name: str, amount: int, inventory: Inventory):
    method = 'post'
    requests_total.labels(method=method).inc()
    start_time = time.time()
    # Increment total purchase attempts in custom metric
    purchase_success_ratio.increment_attempts()
    for item in inventory.items:
        if item.name == name:
            if item.amount < amount:
                latency = time.time() - start_time
                request_latency.labels(method=method).observe(latency)
                request_duration.labels(method=method).observe(latency)
                raise HTTPException(status_code=400, detail="Not enough items in stock")

            # Increment successful purchases in custom metric
            purchase_success_ratio.increment_successes()

            item.amount -= amount
            if item.amount == 0:
                inventory.items.remove(item)
            save_inventory_to_env(inventory)
            low_stock_metric.update_inventory(inventory)
            amount_bought_summary.observe_amount(item.price, amount)
            latency = time.time() - start_time
            request_latency.labels(method=method).observe(latency)
            request_duration.labels(method=method).observe(latency)
            return {"message": f"{amount} units of '{item.name}' purchased successfully", "remaining": item.amount}

    latency = time.time() - start_time
    request_latency.labels(method=method).observe(latency)
    request_duration.labels(method=method).observe(latency)
    raise HTTPException(status_code=404, detail="Item not found")
