
"""Conference room and equipment scheduling system."""

import json
from datetime import datetime

DEFAULT_SCHEDULE_FILE = "schedule.json"
DEFAULT_CONFLICTS_FILE = "conflicts.log"

INITIAL_EQUIPMENT = {
    "projector": 2,
    "microphone": 4,
    "webcam": 1,
}


class RoomScheduler:
    """Manage room reservations, equipment, and booking conflicts."""

    def __init__(self):
        """Initialize reservations and available equipment."""
        self.reservations = {}
        self.equipment_pool = INITIAL_EQUIPMENT.copy()
        self.conflicts = []
        self.next_reservation = 1

    def schedule_room(self, room_id, time_slot, equipment_list=None):
        """Book a room and allocate equipment."""
        if not isinstance(room_id, str) or not room_id.strip():
            raise ValueError("Room ID must be a non-empty string.")

        if equipment_list is None:
            equipment_list = []

        if not isinstance(equipment_list, list):
            raise ValueError("Equipment must be provided as a list.")

        self.slot_hours(time_slot)

        for equipment in equipment_list:
            if equipment not in self.equipment_pool:
                raise ValueError(f"Unknown equipment: {equipment}")

        requested = {}
        for equipment in equipment_list:
            requested[equipment] = requested.get(equipment, 0) + 1

        for equipment, quantity in requested.items():
            if self.equipment_pool[equipment] < quantity:
                raise ValueError(
                    f"Insufficient equipment available: {equipment}"
                )

        for reservation in self.reservations.values():
            if (
                reservation["room"] == room_id
                and reservation["slot"] == time_slot
            ):
                self.conflicts.append(
                    f"{room_id} double-booked at {time_slot}"
                )

        for equipment in equipment_list:
            self.equipment_pool[equipment] -= 1

        reservation_id = self.next_reservation
        self.reservations[reservation_id] = {
            "room": room_id,
            "slot": time_slot,
            "equipment": equipment_list.copy(),
        }
        self.next_reservation += 1

        return reservation_id

    def cancel_reservation(self, reservation_id):
        """Cancel a reservation and return its allocated equipment."""
        reservation = self.reservations.pop(reservation_id, None)

        if reservation is None:
            return False

        for equipment in reservation["equipment"]:
            self.equipment_pool[equipment] += 1

        return True

    @staticmethod
    def slot_hours(time_slot):
        """Return the duration of a valid hour-based time slot."""
        if not isinstance(time_slot, str):
            raise ValueError("Time slot must be a string such as '10-12'.")

        try:
            start_text, end_text = time_slot.split("-")
            start = int(start_text)
            end = int(end_text)
        except ValueError as error:
            raise ValueError(
                "Use a time slot such as '10-12'."
            ) from error

        if start < 0 or start >= end or end > 24:
            raise ValueError(
                "Time slot must have a start before its end, "
                "between hours 0 and 24."
            )

        return end - start

    def export_schedule(self, file=DEFAULT_SCHEDULE_FILE):
        """Export reservations to a JSON file."""
        with open(file, "w", encoding="utf-8") as schedule_file:
            json.dump(self.reservations, schedule_file, indent=4)

    def log_conflicts(self, file=DEFAULT_CONFLICTS_FILE):
        """Append booking conflicts to a log and display the log."""
        with open(file, "a", encoding="utf-8") as log_file:
            for conflict in self.conflicts:
                timestamp = datetime.now().isoformat(timespec="seconds")
                log_file.write(f"{timestamp} {conflict}\n")

        with open(file, "r", encoding="utf-8") as log_file:
            print(log_file.read())


def main():
    """Demonstrate room scheduling and equipment allocation."""
    scheduler = RoomScheduler()

    scheduler.schedule_room("Board-1", "09-11")
    scheduler.schedule_room("Board-1", "09-11")
    reservation_id = scheduler.schedule_room("Huddle-3", "14-16")

    print(
        "Slot length for reservation:",
        scheduler.slot_hours(
            scheduler.reservations[reservation_id]["slot"]
        ),
    )

    if not scheduler.cancel_reservation(77):
        print("Reservation 77 was not found.")

    slot = input(
        "Slot for Board-2, like 10-12 (Enter for 10-12): "
    ).strip() or "10-12"

    try:
        scheduler.schedule_room(
            "Board-2", slot, ["projector", "webcam"]
        )
    except ValueError as error:
        print(f"Booking failed: {error}")

    scheduler.export_schedule()
    scheduler.log_conflicts()

    print("Equipment left:", scheduler.equipment_pool)
    print("Reservations:", scheduler.reservations)


if __name__ == "__main__":
    main()
