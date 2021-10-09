import requests
import json
import os
import re
import io
from datetime import date, timedelta

# environment variables
year = os.getenv('INPUT_YEAR')
leaderboard = os.getenv('INPUT_LEADERBOARD')
session = os.getenv('INPUT_SESSION')
readme = os.getenv('INPUT_FILE')
id = os.getenv('INPUT_USERID')
day_regex = os.getenv('INPUT_DAYREGEX')
stars_regex = os.getenv('INPUT_STARSREGEX')
days_completed_regex = os.getenv('INPUT_DAYSCOMPLETEDREGEX')
if year is None or not leaderboard :
  year = date.today().year
if leaderboard is None or not leaderboard :
  leaderboard = 'https://adventofcode.com/%s/leaderboard/private/view/%s.json' % (year, id)

# fetch stars
cookie = { 'session' : session }
print('Fetching leaderboard data from : ' + leaderboard)
r = requests.get(leaderboard, cookies = cookie)
try:
  data = json.loads(r.text)
except json.JSONDecodeError as err:
  print('Could not parse leaderboard json. Is the leaderboard url correct & your session code valid?')
  print(err)
  exit(1)
stars = data['members'][id]['stars']

# completed days
days_completed = 0
for day in data['members'][id]['completion_day_level']:
  if '2' in data['members'][id]['completion_day_level'][day]:
    days_completed += 1

# current day
today = date.today() - timedelta(hours=5)
day = today.day if today.month == 12 else 24

print('Day: ' + str(day))
print('Stars: ' + str(stars))
print('Days completed: ' + str(days_completed))

# read file
f = io.open(readme, mode='r', encoding='utf-8')
txt = f.read()
f.close()

#replace values
txt = re.sub(day_regex, str(day), txt)
txt = re.sub(stars_regex, str(stars), txt)
txt = re.sub(days_completed_regex, str(days_completed), txt)

# write back file
f = io.open(readme, mode='w', encoding='utf-8')
f.write(txt)
f.close()
