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

def parse_hours(hours_str):
    # Pattern to extract opening hours
    pattern = r'(\w+-\w+|\w+) (\d{1,2}:\d{2} [apm]{2}) - (\d{1,2}:\d{2} [apm]{2})'
    hours = re.findall(pattern, hours_str)
    
    schedule = []
    for days, start, end in hours:
        # Split days if it's a range (e.g., Mon-Thu)
        if '-' in days:
            start_day, end_day = days.split('-')
            start_idx = list(calendar.day_abbr).index(start_day[:3])
            end_idx = list(calendar.day_abbr).index(end_day[:3])
            day_indices = list(range(start_idx, end_idx + 1))
        else:
            day_indices = [list(calendar.day_abbr).index(days[:3])]
        
        for day in day_indices:
            schedule.append({
                'day': day,
                'start': datetime.strptime(start, '%I:%M %p').time(),
                'end': datetime.strptime(end, '%I:%M %p').time()
            })
    
    return schedule

def is_open(schedule, check_time):
    check_day = check_time.weekday()
    check_time_only = check_time.time()
    
    for entry in schedule:
        if entry['day'] == check_day:
            # Handle cases where the end time is past midnight
            if entry['start'] <= check_time_only < entry['end'] or \
               (entry['start'] <= check_time_only or check_time_only < entry['end'] and entry['start'] > entry['end']):
                return True
    return False

def get_open_restaurants(restaurants, check_time):
    open_restaurants = []
    for _, row in restaurants.iterrows():
        name = row['Restaurant Name']
        hours_str = row['Hours']
        schedule = parse_hours(hours_str)
        if is_open(schedule, check_time):
            open_restaurants.append(name)
    return open_restaurants


@app.get("/")
def read_root():
    return 'The application is running! Go to /restaurants to see the open restaurants.'

@app.get("/restaurants")
def get_restaurants(time: Optional[RestaurantTime] = Body(None)):
    # Read the CSV file into a DataFrame
    base_dir = os.path.dirname(__file__)  # Gets the directory where the script is located
    file_path = os.path.join(base_dir, 'data', 'restaurants.csv')  # Constructs the full path
    restaurants = pd.read_csv(file_path)
    if not time or not time.time:
        return {"restaurants": restaurants.to_html()}
    check_time = datetime.strptime(time.time, "%Y-%m-%d %H:%M")
    open_restaurants = get_open_restaurants(restaurants, check_time)
    return {"restaurants": open_restaurants}