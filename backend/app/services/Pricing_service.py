from datetime import datetime
from decimal import Decimal


class PricingService:

    MAX_TOTAL_ADJUSTMENT = Decimal("0.50")

    OCCUPANCY_RULES = [
        (Decimal("0.40"), Decimal("0.00")),
        (Decimal("0.60"), Decimal("0.05")),
        (Decimal("0.80"), Decimal("0.10")),
        (Decimal("1.00"), Decimal("0.15")),
    ]

    DAY_RULES = [
        (30, Decimal("0.00")),
        (14, Decimal("0.05")),
        (7, Decimal("0.10")),
        (0, Decimal("0.15")),
    ]

    @staticmethod
    def calculate_occupancy(
        total_seats: int,
        booked_seats: int,
    ) -> Decimal:
        if total_seats <= 0:
            return Decimal("0")

        occupancy = Decimal(booked_seats) / Decimal(total_seats)

        return min(max(occupancy, Decimal("0")), Decimal("1"))

    @staticmethod
    def get_occupancy_adjustment(
        occupancy: Decimal,
    ) -> Decimal:
        for threshold, adjustment in PricingService.OCCUPANCY_RULES:
            if occupancy <= threshold:
                return adjustment

        return PricingService.OCCUPANCY_RULES[-1][1]

    @staticmethod
    def get_days_adjustment(
        departure_time: datetime,
        now: datetime | None = None,
    ) -> Decimal:

        now = now or datetime.now()

        days_remaining = (
            departure_time - now
        ).total_seconds() / 86400

        for threshold, adjustment in PricingService.DAY_RULES:
            if days_remaining >= threshold:
                return adjustment

        return PricingService.DAY_RULES[-1][1]

    @staticmethod
    def calculate_current_price(
        base_price: Decimal,
        occupancy: Decimal,
        departure_time: datetime,
        now: datetime | None = None,
    ) -> Decimal:

        occupancy_adjustment = (
            PricingService.get_occupancy_adjustment(
                occupancy
            )
        )

        days_adjustment = (
            PricingService.get_days_adjustment(
                departure_time,
                now,
            )
        )

        total_adjustment = (
            occupancy_adjustment
            + days_adjustment
        )

        total_adjustment = min(
            total_adjustment,
            PricingService.MAX_TOTAL_ADJUSTMENT,
        )

        current_price = (
            base_price
            * (Decimal("1") + total_adjustment)
        )

        return current_price.quantize(Decimal("0.01"))