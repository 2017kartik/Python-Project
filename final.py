import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
from collections import Counter
import seaborn as sns


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
    print(tabulate(df, headers='keys', tablefmt='grid'))

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

# Pie Chart
def generate_pie_chart(machines):
    machine_user_counts = {}
    for machine, users in machines.items():
        for user in users:
            key = f"{machine}"
            machine_user_counts[key] = machine_user_counts.get(key, 0) + 1

    machine_user_labels = list(machine_user_counts.keys())
    machine_user_login_counts = list(machine_user_counts.values())
    explode = [0.1 if count == max(machine_user_login_counts) else 0 for count in machine_user_login_counts]
    colors = sns.color_palette("pastel")[:len(machine_user_labels)]

    fig, ax = plt.subplots(figsize=(10, 8))
    plt.pie(
        machine_user_login_counts,
        labels=machine_user_labels,
        explode=explode,
        autopct="%0.1f%%",
        shadow=True,
        radius=1,
        labeldistance=1.1,
        startangle=90,
        textprops={"fontsize": 17, "fontweight": 'bold'},
        counterclock=False,
        wedgeprops={"linewidth": 2},
        rotatelabels=False
    )

    plt.legend(
        machine_user_labels,
        loc='upper center',
        bbox_to_anchor=(1.5, 1.25),
        fontsize=13,
        title_fontproperties={'size': 15, 'weight': 'medium'},
        title="Machine (User)"
    )

    ax.set_position([0.1, 0.005, 0.8, 0.77])
    plt.title("Login Distribution Across Machines and Users", fontsize=26, fontweight='bold', y=0.95)
    plt.show()

#Bar Graph
def generate_bar_graph(events):
    event_data = {
        "date": [event.date for event in events],
        "type": [event.type for event in events],
        "machine": [event.machine for event in events],
        "user": [event.user for event in events]
    }
    df = pd.DataFrame(event_data)
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by='date', inplace=True)

    login_counts = Counter(df[df['type'] == 'login']['machine'])
    logout_counts = Counter(df[df['type'] == 'logout']['machine'])

    machines = sorted(set(login_counts.keys()).union(set(logout_counts.keys())))
    login_values = [login_counts[machine] for machine in machines]
    logout_values = [logout_counts[machine] for machine in machines]

    x = range(len(machines))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.bar(x, login_values, width, label='Logins', color='blue', alpha=0.7)
    ax.bar([i + width for i in x], logout_values, width, label='Logouts', color='green', alpha=0.7)

    ax.set_xticks([i + width / 2 for i in x])
    ax.set_xticklabels(machines, rotation=0, ha="center", fontsize=18)
    ax.set_xlabel('Machines', fontsize=20, fontweight="bold", labelpad=25)
    ax.set_ylabel('Counts', fontsize=20, fontweight="bold", labelpad=25)
    ax.set_title('Login and Logout Counts Per Machine', fontsize=28, fontweight="bold", pad=15)
    ax.yaxis.set_tick_params(labelsize=15)  
    ax.legend(fontsize=15)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

users = current_users(events)
generate_report(users)
generate_pie_chart(users)
generate_bar_graph(events)
