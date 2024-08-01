import calendar
import os
from typing import Optional
from fastapi import Body, FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

import re
from datetime import datetime


class RestaurantTime(BaseModel):
    time: Optional[str] = None


def parse_time(time_str):
    if ":" in time_str:
        return datetime.strptime(time_str, "%I:%M %p").time()
    else:
        return datetime.strptime(time_str, "%I %p").time()


def parse_hours(hours_str):
    # parse pattern from regex
    # pattern = r"(?P<days>[A-Za-z-, ]+)\s+(?P<open_time>\d{1,2}(?::\d{2})? ?[ap]m)\s*-\s*(?P<close_time>\d{1,2}(?::\d{2})? ?[ap]m)"
    pattern = r"(?P<days>[A-Za-z-, ]+)\s+(?P<times>(?:\d{1,2}(?::\d{2})? ?[ap]m\s*-\s*\d{1,2}(?::\d{2})? ?[ap]m\s*(?:\+\s*)?)+)"
    matches = re.finditer(pattern, hours_str)
    # take matches and put into a structure format
    schedule = []
    for match in matches:
        if "," in match.group("days"):
            days = match.group("days").split(", ")
        else:
            days = [match.group("days")]
        for day in days:
            # Split days if it's a range (e.g., Mon-Thu)
            if "-" in day:
                start_day, end_day = day.split("-")
                start_idx = list(calendar.day_abbr).index(start_day.strip()[:3])
                end_idx = list(calendar.day_abbr).index(end_day.strip()[:3])
                day_indices = list(range(start_idx, end_idx + 1))
            else:
                day_indices = [list(calendar.day_abbr).index(day.strip()[:3])]
            
            times = match.group("times").split(" + ")
            for time in times:
                open_time, close_time = time.split(" - ")
                for day in day_indices:
                    schedule.append(
                        {
                            "day": day,
                            "start": parse_time(open_time.strip()),
                            "end": parse_time(close_time.strip()),
                            "after_midnight": parse_time(close_time.strip())
                            < parse_time(open_time.strip()),
                        }
                    )

    return schedule


def is_open(schedule, check_time):
    check_day = check_time.weekday()
    check_time_only = check_time.time()

    for entry in schedule:
        # check if day matches and time is after opening
        if entry["day"] == check_day and check_time_only >= entry["start"]:
            if (
                # time must be before closing or midnight if open after midnight
                check_time_only < entry["end"]
                or (entry["after_midnight"] and check_time_only <= datetime.max.time())
            ):
                return True
        if (
            # check the hours for the day before if it's open after midnight
            entry["day"] == (check_day - 1) % 7
            and entry["after_midnight"]
            # then confirm it's before the start and end
            and check_time_only < entry["end"]
            and check_time_only < entry["start"]
        ):
            return True
    return False


def get_open_restaurants(restaurants, check_time):
    open_restaurants = []
    for _, row in restaurants.iterrows():
        name = row["Restaurant Name"]
        hours_str = row["Hours"]
        schedule = parse_hours(hours_str)
        print(name)
        if is_open(schedule, check_time):
            open_restaurants.append(name)
    return open_restaurants


@app.get("/")
def read_root():
    return "The application is running! Check out our list of restaruants and use the filter to see which ones are open."


@app.post("/restaurants")
def get_restaurants(time: Optional[RestaurantTime] = Body(None)):
    # Read the CSV file into a DataFrame
    base_dir = os.path.dirname(
        __file__
    )  # Gets the directory where the script is located
    file_path = os.path.join(
        base_dir, "data", "restaurants.csv"
    )  # Constructs the full path
    restaurants = pd.read_csv(file_path)
    if not time or not time.time:
        return {"restaurants": restaurants.to_html()}
    check_time = datetime.strptime(time.time, "%Y-%m-%d %H:%M")
    open_restaurants = get_open_restaurants(restaurants, check_time)
    return {"restaurants": open_restaurants}
