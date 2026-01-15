import random

def generate_timetable(room_ids):
    timetable = {}
    OCCUPIED_PROBABILITY = random.uniform(0.8, 0.9)

    for room_id in room_ids:
        timetable[room_id] = []

        if random.random() <= OCCUPIED_PROBABILITY:
            start_hour = random.randint(8, 12)
            duration = random.choice([1, 2, 3, 4])
            end_hour = min(start_hour + duration, 17)

            timetable[room_id].append({
                "start": f"{start_hour:02d}:00",
                "end": f"{end_hour:02d}:00"
            })

    return timetable