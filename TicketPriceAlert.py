import requests, json
# pushover library
from pushover import init, Client

PushoverEnabled = 0

# DCRDATA URL
url="https://dcrdata.decred.org"

# Set Alert Threshold
priceAlertThreshold=200

if (PushoverEnabled):
    config = configparser.ConfigParser()
    config.read("config.ini")
    PushoverToken = config["DEFAULT"]["PushoverToken"]
    PushoverUserKey = config["DEFAULT"]["PushoverUserKey"]
    init(PushoverToken)


try:
    # Get stakediff
    resp = requests.get(url + "/api/stake/diff")
    print(resp.status_code)
    if (resp.status_code != 200):
        print("API Call failed with status code: " + str(resp.status_code))
    else:
        json = json.loads(resp.text)
        ticketPrice=json["current"]
        ticketPriceExpected=json["estimates"]["expected"]

    if (ticketPrice < priceAlertThreshold):
        if (PushoverEnabled):
            Client(PushoverUserKey).send_message('Current price: ' + str(ticketPrice) + ' DCR', title='Ticket Price Below ' + str(priceAlertThreshold))
    else:
        print("Ticket price currently above target threshold: " + str(priceAlertThreshold) + " Currently: "
        + str(ticketPrice) + " Next Window: " + str(ticketPriceExpected))

except:
    print("An exception occurred")
    if (PushoverEnabled):
        Client(PushoverUserKey).send_message('An exception occurred in PushTicketPriceAlert.py', title='Error!')
    quit()
