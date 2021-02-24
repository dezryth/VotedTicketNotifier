# Voted Ticket Notifier
# Track your tickets in a SQLite database and receive 
# notifications as polling discovers they have voted.
# Author: Dezryth
# Created: 02/24/2021
# ------------------------------------------------------------------------
# This script uses the pushover library to send push notifications
# to a mobile device. For more info on setting up and using
# Pushover, please visit: https://pushover.net/
# See the sample-conf.ini for an example config file.
# Once you've added your values in a file named config.ini, set below to 1.
PushoverEnabled = 0
# Feel free to contact me for assistance. Enjoy!
# --------------
# The following is in here for fun if you would like to support my efforts. 
# Set the following to 1 if you want to donate .001 DCR to 
# the author, Dezryth, everytime this script runs and tickets have voted.
# * Wallet must be running unlocked for this to work, if enabled.
# (FYI At $100/DCR, this amounts to 10 cents)
# (No rounding error here. It is greatly appreciated!) (Have you seen my stapler?)
OfficeSpaceMode = 0
# Alternatively, you can send a one-off donation 
# directly to DsfjHsSkgHCygnm5T68n1XNaCBXKD8D8DSZ
# ------------------------------------------------------------------------

import sqlite3, json, collections, subprocess, configparser
from datetime import datetime
from pushover import init, Client

# Initialize SQLite DB if not already present.
conn = sqlite3.connect("tickets.db")
c = conn.cursor()
# Create tickets table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS tickets
            (hash type UNIQUE, dateadded, datevoted)''')

# Get current live tickets according to our database
dbtickets = []
c.execute("SELECT hash FROM tickets WHERE datevoted IS NULL")
select = c.fetchall()
if len(select) > 0:
  dbtickets = list(select[0])
print("db live tickets:\n" + str(dbtickets))

# Get current live tickets according to dcrwallet
tickets = []
getTickets = json.loads(subprocess.check_output("dcrctl --wallet gettickets true", shell=True))
if len(getTickets) > 0:
  tickets = list(getTickets["hashes"])
print("dcrwallet tickets:\n" + str(tickets))

# Compare lists to determine new tickets and voted tickets. 
newTickets = set(tickets) - set(dbtickets)  # Tickets that weren't in the database
if len(newTickets): print("New Tickets:\n" + str(newTickets))
votedTickets = set(dbtickets) - set(tickets) # Tickets that weren't returned by the gettickets command.
if len(votedTickets): print("Voted Tickets:\n" + str(votedTickets))

# Store new ticket hashes in SQLite database if not already present
for x in newTickets:
  now = datetime.now()
  insertCommand = "INSERT INTO tickets(hash, dateadded, datevoted) VALUES('{0}', '{1}', NULL)".format(x, now)
  c.execute(insertCommand)
  conn.commit()

# print("After INSERT:")
# c.execute("SELECT * FROM tickets")
# test = c.fetchall()
# print(test)

# Set existing records that weren't present in response as voted by setting datevoted 
for x in votedTickets:
  now = datetime.now()
  updateCommand = "UPDATE tickets SET datevoted = '{0}' WHERE hash = '{1}'".format(now, x)
  c.execute(updateCommand)
  conn.commit()

# print("After UPDATE:")
# c.execute("SELECT * FROM tickets")
# test = c.fetchall()
# print(test)

# Notify about any voted tickets
if (PushoverEnabled and len(votedTickets) > 0):
  config = configparser.ConfigParser()
  config.read("config.ini")
  PushoverToken = config["DEFAULT"]["PushoverToken"]
  PushoverUserKey = config["DEFAULT"]["PushoverUserKey"]
  init(PushoverToken)
  Client(PushoverUserKey).send_message("The following tickets have voted since last poll:\n" + str(votedTickets), title="DCR Tickets Have Voted")

  # If OfficeSpaceMode is enabled (it is disabled by default), send .001 DCR to Dezryth's address
  if OfficeSpaceMode:
    subprocess.check_output("dcrctl --wallet sendtoaddress DsfjHsSkgHCygnm5T68n1XNaCBXKD8D8DSZ .001", shell=True)
    print("Thanks for your support <3")