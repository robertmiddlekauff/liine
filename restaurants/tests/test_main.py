
from datetime import datetime
import pytest
import pandas as pd
from restaurants.app.main import get_open_restaurants, is_open, parse_hours


def test_parse_hours():
    hours_str = "Mon-Thu 11:00 am - 11:00 pm / Fri-Sat 11:00 am - 12:30 am / Sun 10:00 am - 11:00 pm"
    schedule = parse_hours(hours_str)
    assert len(schedule) == 7  # There should be 7 entries, one for each day
    assert schedule[0]['day'] == 0  # Monday
    assert schedule[0]['start'].strftime("%I:%M %p") == "11:00 AM"
    assert schedule[0]['end'].strftime("%I:%M %p") == "11:00 PM"
    assert schedule[6]['day'] == 6  # Sunday
    assert schedule[6]['start'].strftime("%I:%M %p") == "10:00 AM"
    assert schedule[6]['end'].strftime("%I:%M %p") == "11:00 PM"

def test_is_open():
    schedule = [
        {'day': 0, 'start': datetime.strptime("11:00 am", "%I:%M %p").time(), 'end': datetime.strptime("11:00 pm", "%I:%M %p").time()},
        {'day': 1, 'start': datetime.strptime("11:00 am", "%I:%M %p").time(), 'end': datetime.strptime("11:00 pm", "%I:%M %p").time()},
        {'day': 2, 'start': datetime.strptime("11:00 am", "%I:%M %p").time(), 'end': datetime.strptime("11:00 pm", "%I:%M %p").time()},
        {'day': 3, 'start': datetime.strptime("11:00 am", "%I:%M %p").time(), 'end': datetime.strptime("11:00 pm", "%I:%M %p").time()},
        {'day': 4, 'start': datetime.strptime("11:00 am", "%I:%M %p").time(), 'end': datetime.strptime("12:30 am", "%I:%M %p").time()},
        {'day': 5, 'start': datetime.strptime("11:00 am", "%I:%M %p").time(), 'end': datetime.strptime("12:30 am", "%I:%M %p").time()},
        {'day': 6, 'start': datetime.strptime("10:00 am", "%I:%M %p").time(), 'end': datetime.strptime("11:00 pm", "%I:%M %p").time()},
    ]
    assert is_open(schedule, datetime.strptime("2024-07-29 12:00", "%Y-%m-%d %H:%M"))  # Monday 12:00 PM
    assert not is_open(schedule, datetime.strptime("2024-07-29 10:00", "%Y-%m-%d %H:%M"))  # Monday 10:00 AM
    assert is_open(schedule, datetime.strptime("2024-07-27 23:59", "%Y-%m-%d %H:%M"))  # Saturday 11:59 PM
    assert is_open(schedule, datetime.strptime("2024-07-28 10:00", "%Y-%m-%d %H:%M"))  # Sunday 10:00 AM
    assert not is_open(schedule, datetime.strptime("2024-07-28 09:00", "%Y-%m-%d %H:%M"))  # Sunday 09:00 AM

def test_get_open_restaurants():
    data = {
        "Restaurant Name": ["Restaurant A", "Restaurant B"],
        "Hours": [
            "Mon-Sun 11:00 am - 10:00 pm",
            "Mon-Thu 11:00 am - 11:00 pm / Fri-Sat 11:00 am - 12:30 am / Sun 10:00 am - 11:00 pm"
        ]
    }
    df = pd.DataFrame(data)
    check_time = datetime.strptime("2024-07-30 22:00", "%Y-%m-%d %H:%M")  # Tuesday 10:00 PM

    open_restaurants = get_open_restaurants(df, check_time)
    assert open_restaurants == ["Restaurant A", "Restaurant B"]

    check_time = datetime.strptime("2024-07-30 23:00", "%Y-%m-%d %H:%M")  # Tuesday 11:00 PM
    open_restaurants = get_open_restaurants(df, check_time)
    assert open_restaurants == ["Restaurant A", "Restaurant B"]

    check_time = datetime.strptime("2024-07-28 09:00", "%Y-%m-%d %H:%M")  # Sunday 09:00 AM
    open_restaurants = get_open_restaurants(df, check_time)
    assert open_restaurants == []