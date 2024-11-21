import numpy as np
import pandas as pd

def get_event_date(event):
    return event.date

def current_users(events):
  
    event_data = {
        "date": [event.date for event in events],
        "type": [event.type for event in events],
        "machine": [event.machine for event in events],
        "user": [event.user for event in events]
    }
    df = pd.DataFrame(event_data)
    
  
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by='date', inplace=True)

    machines = {}
    for _, row in df.iterrows():
        machine = row['machine']
        user = row['user']
        if machine not in machines:
            machines[machine] = set()
        if row['type'] == "login":
            machines[machine].add(user)
        elif row['type'] == "logout":
            machines[machine].discard(user) 
    return machines

def generate_report(machines):
    for machine, users in machines.items():
        if len(users) > 0:
            user_list = ", ".join(users)
            print("{}: {}".format(machine, user_list))

class Event:
    def __init__(self, event_date, event_type, machine_name, user):
        self.date = event_date
        self.type = event_type
        self.machine = machine_name
        self.user = user

events = [
    Event('2024-09-01 12:45:56', 'login', 'myworkstation.local', 'jordan'),
    Event('2024-09-02 15:53:42', 'logout', 'webserver.local', 'jordan'),
    Event('2024-09-01 18:53:21', 'login', 'webserver.local', 'lane'),   
    Event('2024-09-02 10:25:34', 'logout', 'myworkstation.local', 'jordan'),
    Event('2024-09-01 08:20:01', 'login', 'webserver.local', 'jordan'),
    Event('2024-09-03 11:24:35', 'login', 'mailserver.local', 'chris'),
]

users = current_users(events)
generate_report(users)
