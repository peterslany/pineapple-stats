import json
import pickle
import os
import datetime
import plotly
import plotly.graph_objs as go
from participant import Participant, Content

# This code proccess data and make new ones going throught all of the
# messages. Input is JSON file from facebook, please put it into the repository.
# 
# It takes from few seconds to minutes to make the output file for the 
# statistics due to the amount of messages in the group. You will get message.

# Change of working directory to location of this file.
os.chdir(os.path.dirname(os.path.realpath(__file__))) 

# Converts data from JSON file into python dictionary.
with open('message.json', encoding='raw_unicode_escape') as json_data:
    data = json.loads(json_data.read().encode('raw_unicode_escape').decode(), strict=False)
participants = {}

for person in data['participants']:
    participants[person['name']] = Participant(person['name'])

all = Participant('all')
member_count = len(participants)
avg = Participant('average')


for message in data['messages']:
    participants[message['sender_name']].add_message(message)
    all.add_message(message)

for content in all.content:
    for period in all.content[content].period:
        for item in all.content[content].period[period]:
            avg.content[content].period[period][item] = round(
                all.content[content].period[period][item]/member_count, 2)
    avg.content[content].total = round(all.content[content].total/member_count, 2)

sorted_time = Content('sorted_time')
sorted_time.period['month'] = {'January':0,'February':0,'March':0,'April':0,
                               'May':0,'June':0,'July':0,'August':0,'September':0,
                               'October':0,'November':0, 'December':0}
sorted_time.period['week_day'] = {'Monday':0,'Tuesday':0,'Wednesday':0,
                                  'Thursday':0,'Friday':0,'Saturday':0,'Sunday':0}
sorted_time.period['hour'] = {'00' : 0, '01' : 0, '02': 0, '03': 0, '04': 0, '05': 0, 
                              '06': 0, '07':0, '08': 0, '09' : 0, '10' : 0, '11' : 0,
                             '12' : 0, '13' :0, '14' : 0, '15' : 0, '16' : 0, '17': 0,
                             '18' :0, '19':0, '20':0,'21':0,'22':0,'23':0}

last_message = datetime.datetime.fromtimestamp(int(str(data['messages'][0]['timestamp_ms'])[:-3]))
first_message = datetime.datetime.fromtimestamp(int(str(message['timestamp_ms'])[:-3]))

while first_message < last_message:
    sorted_time.add_entry(first_message ,datetime_object=True)
    first_message += datetime.timedelta(days=1)

data = {'participants' : participants, 'all' : all, 'sorted_time' : sorted_time, 
        'average' : avg, 'title' : data['title']}

print("DATA PROCCESSED SUCCESSFULLY!")

with open('structured_data.pickle', 'wb') as data_out:
    pickle.dump(data, data_out)

print("DATA SAVED SUCCESSFULLY INTO THE FILE: structured_data.pickle!")