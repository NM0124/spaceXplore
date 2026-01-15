from datetime import datetime, timedelta, time as time_obj

BUFFER_MINUTES = 5

def get_status(room_id, timetable, demo_time, overrides=None):
    h, m = map(int, demo_time.split(":"))
    now = time_obj(h, m)

    if overrides:
        for o in overrides:
            if o["room_id"] != room_id:
                continue

            start = time_obj(*map(int, o["start_time"].split(":")))
            end = time_obj(*map(int, o["end_time"].split(":")))

            if start <= now <= end:
                if o["type"] == "occupied":
                    next_available = (
                        datetime.combine(datetime.today(), end)
                        + timedelta(minutes=BUFFER_MINUTES)
                    ).strftime("%I:%M %p")
                    return "Occupied", next_available

                if o["type"] == "available":
                    return "Available", None

    sessions = timetable.get(room_id, [])

    for s in sessions:
        sh, sm = map(int, s["start"].split(":"))
        eh, em = map(int, s["end"].split(":"))
        start = time_obj(sh, sm)
        end = time_obj(eh, em)

        if start <= now <= end:
            next_available = (
                datetime.combine(datetime.today(), end)
                + timedelta(minutes=BUFFER_MINUTES)
            ).strftime("%I:%M %p")
            return "Occupied", next_available

    return "Available", None