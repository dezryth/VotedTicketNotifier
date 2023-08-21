import sqlite3, configparser, calendar

from datetime import datetime
from pushover import init, Client

PushoverEnabled = 1

conn = sqlite3.connect("tickets.db")
c = conn.cursor()

# Get Voted Tickets
dbtickets = []
c.execute("SELECT round(julianday(datevoted) - julianday(dateadded), 0) AS numlivedays, datevoted AS datevoted, hash FROM tickets WHERE datevoted IS NOT NULL ORDER BY datevoted DESC")
select = [row for row in c.fetchall()]
dbtickets = list(select)
#print(dbtickets)

c.execute("SELECT strftime('%m', datevoted) AS monthvoted, count(*) numvotes FROM tickets WHERE datevoted IS NOT NULL AND strftime('%Y', datevoted) = strftime('%Y', 'now') GROUP BY monthvoted ORDER BY mon
thvoted DESC LIMIT 6")
select = [row for row in c.fetchall()]
monthlyvotes = list(select)
#print(monthlyvotes)

message = ""

# Format Voted Tickets
votedtickets = "# Days Live, Hash:\n"
for x in dbtickets:
  votedtickets += str(x).replace("(","").replace(")","") + "\n"
#print(votedtickets)

# Get Average days to vote
sumdays = 0
for x in dbtickets:
  sumdays += x[0]
average = sumdays / len(dbtickets)
message += "Avg days to vote: " + str(round(average, 2)) + "\n"

# Get Average votes per month
votespermonth = "Votes Per Month - Last 6 Months\n"
for x in monthlyvotes:
  votespermonth += calendar.month_name[int(x[0])] + ": " + str(x[1]) + "\n"
message += votespermonth

print(message)

# Send Push Notification about Live Tickets
if (PushoverEnabled and len(dbtickets) > 0):
  config = configparser.ConfigParser()
  config.read("config.ini")
  PushoverToken = config["DEFAULT"]["PushoverToken"]
  PushoverUserKey = config["DEFAULT"]["PushoverUserKey"]
  init(PushoverToken)
  Client(PushoverUserKey).send_message(message, title="DCR Tickets Misc")
