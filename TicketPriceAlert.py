import requests, json, configparser
# pushover library
from pushover import init, Client

PushoverEnabled = 0

# DCRDATA URL
url="https://dcrdata.decred.org"

# Set Alert Thresholds
priceAlertThreshold=200
poolSizeTargetDiffThreshold=-5
poolTarget=40960

if (PushoverEnabled):
    config = configparser.ConfigParser()
    config.read("config.ini")
    PushoverToken = config["DEFAULT"]["PushoverToken"]
    PushoverUserKey = config["DEFAULT"]["PushoverUserKey"]
    init(PushoverToken)

try:
    # Get stakediff
    resp = requests.get(url + "/api/stake/diff")
    print("api/stake/diff: " + str(resp.status_code))
    if (resp.status_code != 200):
        print("API Call failed with status code: " + str(resp.status_code))
    else:
        pricejson = json.loads(resp.text)
        ticketPrice = pricejson["current"]
        ticketPriceExpected = pricejson["estimates"]["expected"]
    
    if (ticketPrice < priceAlertThreshold):
        if (PushoverEnabled):
            Client(PushoverUserKey).send_message('Current price: ' + str(ticketPrice) + ' DCR', title='Ticket Price Below ' + str(priceAlertThreshold))
    else:
        print("Ticket price currently above target threshold: " + str(priceAlertThreshold) + " Currently: "
        + str(ticketPrice) + " Next Window: " + str(ticketPriceExpected))

    # Get ticket pool size
    resp = requests.get(url + "/api/stake/pool")
    print("/api/stake/pool: " + str(resp.status_code))
    if (resp.status_code != 200):
        print("API Call failed with status code: " + str(resp.status_code))
    else:
        pooljson = json.loads(resp.text)
        poolSize = pooljson["size"]
        targetDiff = ((poolSize / poolTarget) - 1) * 100
    print("Pool Size Target Diff: " + str(round(targetDiff, 2)) + "%")

    if (targetDiff < poolSizeTargetDiffThreshold):
        if (PushoverEnabled):
            Client(PushoverUserKey).send_message("Ticket Pool Size Under Target by " + str(round(targetDiff, 2)) + '%', title='Ticket Pool Alert')

except Exception as e:
    print("An exception occurred: ", e)
    if (PushoverEnabled):
        Client(PushoverUserKey).send_message('An exception occurred in PushTicketPriceAlert.py', title='Error!')
    quit()
