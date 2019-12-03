from django.contrib import admin

from . import models


@admin.register(models.NewsSubscription)
class NewsSubscriptionAdmin(admin.ModelAdmin):

    list_display = ("time", "email")
    list_filter = ("email", )


@admin.register(models.TokenMetric)
class TokenMetricAdmin(admin.ModelAdmin):

    list_display = ("timestamp", "rank", "price_usd", "market_cap_usd", "available_supply")
