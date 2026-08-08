from src.posting_period_service import (
    close_period,
    is_period_open,
    open_period,
)

def run_tests() -> None:
    print("August initially open:")
    print(is_period_open("UK01", 2026, 8))

    print("\nClosing August:")
    closed_period = close_period("UK01", 2026, 8)
    print(closed_period)

    print("\nAugust after closing:")
    print(is_period_open("UK01", 2026, 8))

    print("\nReopening August:")
    opened_period = open_period("UK01", 2026, 8)
    print(opened_period)

    print("\nAugust after reopening:")
    print(is_period_open("UK01", 2026, 8))

    print("\nOpening September:")
    september_period = open_period("UK01", 2026, 9)
    print(september_period)


if __name__ == "__main__":
    run_tests()