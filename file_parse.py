from collections import defaultdict
import csv
from datetime import datetime as dt, timezone
from security_history import SecurityHistory


def parse_file(filepath) -> dict[str, SecurityHistory]:
    securities = defaultdict(SecurityHistory)

    def process_row(
        datetime: "dt",
        action: str,
        security_symbol: str,
        transaction_total: float,
        share_count: int,
    ):
        # todo - until we can deal with dividends and stuff
        if action.lower() not in ["buy", "sell"]:
            return

        security = securities[security_symbol]

        match action.lower():
            case "buy":
                security.buy(datetime, transaction_total / share_count, share_count)
            case "sell":
                security.sell(datetime, transaction_total / share_count, share_count)
            case _:
                pass

    with open(filepath) as csvfile:
        reader = csv.reader(csvfile)

        # skip header
        next(reader, None)

        for (
            datetime,
            action,
            security_symbol,
            transaction_total,
            share_count,
            description,
        ) in sorted(reader, key=lambda row: row[0]):
            process_row(
                dt.fromisoformat(datetime).replace(tzinfo=timezone.utc),
                action,
                security_symbol,
                abs(float(transaction_total)),
                abs(float(share_count)),
            )

    return securities
