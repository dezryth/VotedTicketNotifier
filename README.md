# Voted Ticket Notifier

This is a simple Python script for setting yourself up with a way to receive notifications once your tickets have voted.

The script uses the Python library for [Pushover](https://pushover.net/ "Pushover") in order to send push notifications to your mobile device.

### How to get started
1. Copy and rename `sample-config.ini` to `config.ini`
2. Replace the values with your Pushover Token and User Key
3. Using your preferred method, set up a script to run this script on an recurring schedule (e.g. every 15 minutes)
4. Wait for tickets to vote!

### How it works

The script works by creating a simple SQLite database that stores ticket hashes returned by the `dcrctl --wallet gettickets true` command, and comparing records that already exist in the database to future calls to that same command. Once the hash falls off the returned results, it can be assumed that ticket has voted. The record corresponding to that address is updated as having been voted, and then the script sends you a push notification informing you of voted tickets.

**Please review the script yourself and do not run until you are comfortable with what it is doing. The script is commented to simplify this.**

This was mostly for fun and to help give others a tool to keep track of their tickets as they vote. Please learn what you can from it and modify it for your particular needs. Pull requests will be appreciated!

If you *really* appreciate this script, you can tip me DCR at DsfjHsSkgHCygnm5T68n1XNaCBXKD8D8DSZ, or you can enable OfficeSpaceMode in the script by setting `OfficeSpaceMode = 1`
This will send .001 DCR to my donation address each time the script finds tickets that have voted, which would amounts to about 15 cents while DCR is worth $150. No pressure!

Have you seen my stapler?