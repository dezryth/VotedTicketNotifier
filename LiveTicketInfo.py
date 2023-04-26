import sqlite3, configparser                                                                                                                                                                         
                                                                                                                                                                                                     
from datetime import datetime                                                                                                                                                                        
from pushover import init, Client                                                                                                                                                                    
                                                                                                                                                                                                     
PushoverEnabled = 1                                                                                                                                                                                  
                                                                                                                                                                                                     
conn = sqlite3.connect("tickets.db")                                                                                                                                                                 
c = conn.cursor()                                                                                                                                                                                    
                                                                                                                                                                                                     
# Get Live Tickets                                                                                                                                                                                   
dbtickets = []                                                                                                                                                                                       
c.execute("SELECT round(julianday('now') - julianday(dateadded), 0) AS numlivedays, hash FROM tickets WHERE datevoted IS NULL ORDER BY numlivedays DESC")                                            
select = [row for row in c.fetchall()]                                                                                                                                                               
if len(select) > 0:                                                                                                                                                                                  
  dbtickets = list(select)                                                                                                                                                                           
                                                                                                                                                                                                     
# Format Live Tickets                                                                                                                                                                                
livetickets = "# Days Live, Hash:\n"                                                                                                                                                                 
for x in dbtickets:                                                                                                                                                                                  
  livetickets += str(x).replace("(","").replace(")","") + '\n'                                                                                                                                       
                                                                                                                                                                                                     
print(livetickets)                                                                                                                                                                                   
                                                                                                                                                                                                     
# Send Push Notification about Live Tickets                                                                                                                                                          
if (PushoverEnabled and len(dbtickets) > 0):                                                                                                                                                         
  config = configparser.ConfigParser()                                                                                                                                                               
  config.read("config.ini")                                                                                                                                                                          
  PushoverToken = config["DEFAULT"]["PushoverToken"]                                                                                                                                                 
  PushoverUserKey = config["DEFAULT"]["PushoverUserKey"]                                                                                                                                             
  init(PushoverToken)                                                                                                                                                                                
  Client(PushoverUserKey).send_message(livetickets, title="DCR Tickets Status")
