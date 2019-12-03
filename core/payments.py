from decimal import Decimal

from django.conf import settings

import slumber

import structlog

logger = structlog.getLogger()

assert not settings.PAYMENTS_API_URL.endswith("/")

api = slumber.API(settings.PAYMENTS_API_URL, auth=settings.PAYMENTS_API_AUTH, append_slash=False)


class PaymentsServiceError(Exception):
    def __init__(self, message, user_message=None, details=None):
        self.message = message
        self.user_message = user_message
        self.details = details
        super(PaymentsServiceError, self).__init__(message, user_message, details)


def get_balance_tokens(wallet):
    try:
        data = api.blockchains.eth.get_balance_tokens(wallet).get()
        balance = Decimal(data["balance"])
        logger.bind(wallet=wallet, balance=balance).debug("Wallet current balance")
        return balance
    except Exception as e:
        logger.bind(wallet=wallet, url=settings.PAYMENTS_API_URL).exception("Error communicate with payments service")
        raise PaymentsServiceError(f"Failed to communicate with the remote service: {repr(e)}",
                                   user_message="ERRP001: Internal server issue")


def get_hodl_interest(wallet):
    try:
        data = api.blockchains.eth.get_hodl_interest(wallet).get()
        interest = Decimal(data["interest"])
        logger.bind(wallet=wallet, interest=interest)
        return interest
    except Exception as e:
        logger.bind(wallet=wallet, url=settings.PAYMENTS_API_URL).exception("Error communicate with payments service")
        raise PaymentsServiceError(f"Failed to communicate with the remote service: {repr(e)}",
                                   user_message="ERRP002: Internal server issue")
