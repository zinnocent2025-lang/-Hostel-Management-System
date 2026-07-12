from core.models import ExternalRoom

rooms = ExternalRoom.objects.select_related("hostel").order_by("hostel_id", "id")

current_hostel = None
counter = 1

for room in rooms:
    if room.hostel_id != current_hostel:
        current_hostel = room.hostel_id
        counter = 1

    prefix = "".join(word[0] for word in room.hostel.name.split()[:3]).upper()

    room.room_number = f"{prefix}{counter:03d}"
    room.save(update_fields=["room_number"])

    print(f"{room.hostel.name} -> {room.room_number}")

    counter += 1

print("Finished!")
