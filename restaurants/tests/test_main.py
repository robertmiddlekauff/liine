from datetime import datetime
import pandas as pd

from restaurants.app.main import get_open_restaurants, is_open, parse_hours


def test_parse_hours():
    hours_str = "Mon-Thu 11:00 am - 8:00 pm + 9:00 pm - 10:00 pm / Fri-Sat 11:00 am - 12:30 am / Sun 10:00 am - 11:00 pm"
    schedule = parse_hours(hours_str)
    print(schedule)
    assert len(schedule) == 11  # There should be 7 entries, one for each day
    assert schedule[0]["day"] == 0  # Monday
    assert schedule[0]["start"].strftime("%I:%M %p") == "11:00 AM"
    assert schedule[0]["end"].strftime("%I:%M %p") == "08:00 PM"
    assert schedule[0]["after_midnight"] == False
    assert schedule[9]["after_midnight"]  # Saturday should have after_midnight set to True
    assert schedule[10]["day"] == 6  # Sunday
    assert schedule[10]["start"].strftime("%I:%M %p") == "10:00 AM"
    assert schedule[10]["end"].strftime("%I:%M %p") == "11:00 PM"


def test_is_open():
    schedule = [
        {
            "day": 0,
            "start": datetime.strptime("11:00 am", "%I:%M %p").time(),
            "end": datetime.strptime("11:00 pm", "%I:%M %p").time(),
            "after_midnight": False,
        },
        {
            "day": 1,
            "start": datetime.strptime("11:00 am", "%I:%M %p").time(),
            "end": datetime.strptime("11:00 pm", "%I:%M %p").time(),
            "after_midnight": False,
        },
        {
            "day": 2,
            "start": datetime.strptime("11:00 am", "%I:%M %p").time(),
            "end": datetime.strptime("11:00 pm", "%I:%M %p").time(),
            "after_midnight": False,
        },
        {
            "day": 3,
            "start": datetime.strptime("11:00 am", "%I:%M %p").time(),
            "end": datetime.strptime("11:00 pm", "%I:%M %p").time(),
            "after_midnight": False,
        },
        {
            "day": 4,
            "start": datetime.strptime("11:00 am", "%I:%M %p").time(),
            "end": datetime.strptime("12:30 am", "%I:%M %p").time(),
            "after_midnight": True,
        },
        {
            "day": 5,
            "start": datetime.strptime("11:00 am", "%I:%M %p").time(),
            "end": datetime.strptime("12:30 am", "%I:%M %p").time(),
            "after_midnight": True,
        },
        {
            "day": 6,
            "start": datetime.strptime("10:00 am", "%I:%M %p").time(),
            "end": datetime.strptime("11:00 pm", "%I:%M %p").time(),
            "after_midnight": False,
        },
    ]
    assert is_open(
        schedule, datetime.strptime("2024-07-29 12:00", "%Y-%m-%d %H:%M")
    )  # Monday 12:00 PM
    assert not is_open(
        schedule, datetime.strptime("2024-07-29 23:30", "%Y-%m-%d %H:%M")
    )  # Monday 11:30 PM
    assert not is_open(
        schedule, datetime.strptime("2024-07-29 10:00", "%Y-%m-%d %H:%M")
    )  # Monday 10:00 AM
    assert not is_open(
        schedule, datetime.strptime("2024-07-30 00:00", "%Y-%m-%d %H:%M")
    )  # Tuesday at midnight
    assert not is_open(
        schedule, datetime.strptime("2024-07-26 00:15", "%Y-%m-%d %H:%M")
    )  # Friday 12:15 AM
    assert is_open(
        schedule, datetime.strptime("2024-07-27 00:15", "%Y-%m-%d %H:%M")
    )  # Saturday 12:15 AM
    assert is_open(
        schedule, datetime.strptime("2024-07-27 23:59", "%Y-%m-%d %H:%M")
    )  # Saturday 11:59 PM
    assert not is_open(
        schedule, datetime.strptime("2024-07-28 09:00", "%Y-%m-%d %H:%M")
    )  # Sunday 09:00 AM
    assert is_open(
        schedule, datetime.strptime("2024-07-28 10:00", "%Y-%m-%d %H:%M")
    )  # Sunday 10:00 AM
    assert is_open(
        schedule, datetime.strptime("2024-07-28 00:15", "%Y-%m-%d %H:%M")
    )  # Sunday 10:00 AM


def test_get_open_restaurants():
    data = {
        "Restaurant Name": ["Restaurant A", "Restaurant B"],
        "Hours": [
            "Mon-Sun 11:00 am - 10:00 pm",
            "Mon-Thu 11:00 am - 11:00 pm / Fri-Sat 11:00 am - 12:30 am / Sun 10:00 am - 11:00 pm",
        ],
    }
    df = pd.DataFrame(data)
    check_time = datetime.strptime(
        "2024-07-30 22:00", "%Y-%m-%d %H:%M"
    )  # Tuesday 10:00 PM

    open_restaurants = get_open_restaurants(df, check_time)
    assert open_restaurants == ["Restaurant B"]

    check_time = datetime.strptime(
        "2024-07-30 23:00", "%Y-%m-%d %H:%M"
    )  # Tuesday 11:00 PM
    open_restaurants = get_open_restaurants(df, check_time)
    assert open_restaurants == []

    check_time = datetime.strptime(
        "2024-07-28 00:15", "%Y-%m-%d %H:%M"
    )  # Sunday 09:00 AM
    open_restaurants = get_open_restaurants(df, check_time)
    assert open_restaurants == ["Restaurant B"]
    
    check_time = datetime.strptime(
        "2024-07-28 12:00", "%Y-%m-%d %H:%M"
    )  # Sunday 09:00 AM
    open_restaurants = get_open_restaurants(df, check_time)
    assert open_restaurants == ["Restaurant A", "Restaurant B"]
