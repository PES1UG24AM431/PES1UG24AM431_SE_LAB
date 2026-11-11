
def parse_zone(text):
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    parts = text.split(':')
    if len(parts) != 2:
        raise ValueError("Expected format: zone:area")

    name = parts[0].strip()
    if not name:
        raise ValueError("Zone name cannot be empty")

    try:
        area = float(parts[1].strip())
    except ValueError:
        raise ValueError("Area must be numeric")

    if not name or area <= 0 or not area < float('inf'):
        raise ValueError("Invalid zone name or area")

    return name.title(), area


def moisture_average(readings_csv):
    if not isinstance(readings_csv, str) or not readings_csv.strip():
        raise ValueError("Readings must be a non-empty CSV string")

    try:
        values = [int(r.strip()) for r in readings_csv.split(',')]
    except ValueError:
        raise ValueError("Readings must contain valid integers")

    if not values:
        raise ValueError("At least one reading is required")

    if any(value < 0 or value > 100 for value in values):
        raise ValueError("Moisture readings must be between 0 and 100")

    return sum(values) // len(values)


def water_needed(text):
    if not isinstance(text, str):
        raise ValueError("Input must be a string")

    parts = text.split('|')
    if len(parts) != 2:
        raise ValueError("Expected format: area|rainfall")

    try:
        plot = float(parts[0].strip())
        rain = float(parts[1].strip())
    except ValueError:
        raise ValueError("Area and rainfall must be numeric")

    if not (0 < plot < float('inf')) or not (0 <= rain < float('inf')):
        raise ValueError("Area must be positive and rainfall non-negative")

    need = plot * 5 - rain
    return max(need, 0)


def main():
    print("==== Running parse_zone ====")
    user_input = input("Enter zone:area in m2 (e.g. north:120): ")
    print("Zone and Area:", parse_zone(user_input))

    print("\n==== Running moisture_average ====")
    user_input = input("Enter moisture readings as CSV (e.g. 40,35,50): ")
    print("Average Moisture:", moisture_average(user_input))

    print("\n==== Running water_needed ====")
    user_input = input("Enter area|rainfall (e.g. 120|8): ")
    print("Water Needed:", water_needed(user_input))


if __name__ == "__main__":
    main()
