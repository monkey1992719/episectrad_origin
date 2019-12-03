from celery import shared_task

import requests

import structlog

from . import models

logger = structlog.get_logger()


@shared_task
def update_token_metrics():
    res = requests.get("https://api.coinmarketcap.com/v1/ticker/education-ecosystem/")
    data = res.json()
    if data and "error" not in data[0]:
        d = data[0]
        update = {"rank": d.get("rank"),
                  "price_usd": d.get("price_usd"),
                  "price_btc": d.get("price_btc"),
                  "day_volume_usd": d.get("24h_volume_usd"),
                  "market_cap_usd": d.get("market_cap_usd"),
                  "available_supply": d.get("available_supply"),
                  "total_supply": d.get("total_supply"),
                  "percent_change_1h": d.get("percent_change_1h", 0),
                  "percent_change_24h": d.get("percent_change_24h", 0),
                  "percent_change_7d": d.get("percent_change_7d", 0)}
        models.TokenMetric.objects.create(**update)
        logger.bind(**update).info("Updating metrics from coinmarketcap.com")
