import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone

# Load CSV files into DataFrames
csv_a = pd.read_csv('servicenow.csv')
csv_b = pd.read_csv('event_history 349788422230.csv')

# # Define the target event names array
targetEventsArr = [
    'CreateSnapshot',
    'DeleteDBInstance',
    'TerminateInstances',
    'StartConfigurationRecorder',
    'PutDeliveryChannel',
    'PutConfigurationRecorder',
    'UpdateStack',
    'CreateStack',
    'DeleteStack',
    'ModifyDBInstance',
    'StartDBInstance',
    'StopDBInstance',
    'ReleaseAddress',
    'RotateKey',
    'DeleteKey'
]

# targetEventsArr = [
#     'ModifyDBInstance',
#     'StartDBInstance',
#     'StopDBInstance',
#     'ReleaseAddress',
#     'RotateKey',
#     'DeleteKey'
# ]

# Convert string date/time to datetime objects with custom formats
csv_a['Planned start date'] = pd.to_datetime(csv_a['Planned start date'], format='%Y-%m-%d %H:%M:%S')
csv_a['Planned end date'] = pd.to_datetime(csv_a['Planned end date'], format='%Y-%m-%d %H:%M:%S')
csv_b['Event time'] = pd.to_datetime(csv_b['Event time']) + timedelta(hours=8) 
# Convert csv_a timestamps to timezone-aware timestamps
csv_a['Planned start date'] = csv_a['Planned start date'].apply(lambda x: x.replace(tzinfo=timezone('UTC')))
csv_a['Planned end date'] = csv_a['Planned end date'].apply(lambda x: x.replace(tzinfo=timezone('UTC')))

# Iterate through rows of csv_b
for index, row_b in csv_b.iterrows():
    event_name = row_b['Event name']
    
    if event_name in targetEventsArr:
        # event_time = row_b['Event time']- timedelta(days=90) 
        event_time = row_b['Event time']
        
        # Check if event time falls within any range in csv_a
        event_found = False
        for _, row_a in csv_a.iterrows():
            time_difference = row_a['Planned end date'] - row_a['Planned start date']
            if row_a['Planned start date'] <= event_time <= row_a['Planned end date'] and time_difference.days <= 2:
                event_found = True
                print(f"Change ticket found for {event_name} for event ID {row_b['Event ID']} at timestamp {row_b['Event time']}, change number: {row_a['Number']}, change window: {row_a['Planned start date']} {row_a['Planned end date']}")
                break
        
        # if not event_found:
        #     print(f"Change ticket not found for {event_name} for event ID {row_b['Event ID']}")
    # else:
        # print(f"Event name {event_name} not in targetEventsArr")
