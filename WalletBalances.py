import json, subprocess, configparser                                                                                                                                                                
from datetime import datetime                                                                                                                                                                        
from pushover import init, Client                                                                                                                                                                    
                                                                                                                                                                                                     
PushoverEnabled = 1                                                                                                                                                                                  
                                                                                                                                                                                                     
walletDetails = json.loads(subprocess.check_output("dcrctl --wallet getbalance", shell=True))                                                                                                        
                                                                                                                                                                                                     
if len(walletDetails) > 0:                                                                                                                                                                           
  lockedByTickets = walletDetails["totallockedbytickets"]                                                                                                                                            
  spendable = walletDetails["totalspendable"]                                                                                                                                                        
  total = walletDetails["cumulativetotal"]                                                                                                                                                           
                                                                                                                                                                                                     
strWalletBalance = "Locked By Tickets: " + str(lockedByTickets) + "\n" + "Spendable: " + str(spendable) + "\n" + "Total: " + str(total)                                                              
                                                                                                                                                                                                     
print(strWalletBalance)                                                                                                                                                                              
                                                                                                                                                                                                     
if (PushoverEnabled and len(walletDetails) > 0):                                                                                                                                                     
  config = configparser.ConfigParser()                                                                                                                                                               
  config.read("config.ini")                                                                                                                                                                          
                                                                                                                                                                                                     
  PushoverToken = config["DEFAULT"]["PushoverToken"]                                                                                                                                                 
  PushoverUserKey = config["DEFAULT"]["PushoverUserKey"]                                                                                                                                             
  init(PushoverToken)                                                                                                                                                                                
                                                                                                                                                                                                     
  Client(PushoverUserKey).send_message(strWalletBalance, title="DCR Wallet Balance")
