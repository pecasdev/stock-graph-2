from collections import defaultdict
from security_history import SecurityHistory
from stock_api import StockApi
from datetime import datetime as dt, timedelta
from datetime import timezone
from pytz import timezone as pytz


def _calculate_history_start_date(security_history_list: list[SecurityHistory]):
    smallest_date = dt.now().replace(tzinfo=timezone.utc)

    for security_history in security_history_list:
        smallest_date = min(smallest_date, min(security_history.history.keys()))

    return smallest_date


def calculate_profit_history(security_symbol_to_history: dict[str, SecurityHistory]):
    profit_history = defaultdict(dict[str, int])

    history_start_date = _calculate_history_start_date(
        security_symbol_to_history.values()
    )

    # markets close at 8pm UTC so we want to consider everything up to 8pm for any given day
    history_start_date = history_start_date.replace(hour=20, minute=0, second=0)

    history_end_date = dt.now().replace(tzinfo=timezone.utc)

    stock_api = StockApi(history_start_date, history_end_date)

    current_iteration_date = history_start_date
    while current_iteration_date <= history_end_date:
        for security_symbol, security_history in security_symbol_to_history.items():
            most_recent_entry = security_history.last_entry_before_or_at_datetime(
                current_iteration_date
            )

            if most_recent_entry is None:
                # we might not have traded this stock yet at the current moment in time
                continue

            [share_count, total_share_cost] = most_recent_entry

            closing_price = stock_api.getClosePriceOnDate(
                security_symbol, current_iteration_date
            )

            if closing_price is None:
                # it is possibly the weekend/holiday, no closing prices are available
                break

            profit = (share_count * closing_price) - total_share_cost
            profit_history[current_iteration_date][security_symbol] = profit

        current_iteration_date += timedelta(days=1)

    return profit_history
