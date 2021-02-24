# Voted Ticket Notifier

This is a simple Python script for setting yourself up with a way to receive notifications once your tickets have voted.

The script uses the Python library for [Pushover](https://pushover.net/ "Pushover") to send push notifications to your mobile device. You will want to install the Pushover app to your phone if you choose to use this notification method.

* This README is likely to change as I receive feedback to lower the bar and make the setup even easier.

### How to get started
1. Copy and rename `sample-config.ini` to `config.ini`.
2. Install the python pushover library with command `pip install python-pushover`
2. Replace the values with your Pushover Token and User Key.
3. Using your preferred method, set up a script to run this script on a recurring schedule (e.g. every 15 minutes). See `RunVotedTicketNotifier.sh` for an example bash script. You can run in a tmux session to keep
the process going after you exit an ssh session. (e.g. `tmux new -s ticknotif '~/VotedTicketNotifier/RunVotedTicketNotifier.sh'`)
4. Wait for tickets to vote and to receive notifications!

### How it works

The script works by creating a simple SQLite database that stores ticket hashes returned by the `dcrctl --wallet gettickets true` command, and comparing records that already exist in the database to future calls to that same command. Once the hash falls off the returned results, it can be assumed that ticket has voted. The record corresponding to that address is updated as having been voted, and then the script sends you a push notification informing you of voted tickets.

**Please review the script yourself and do not run until you are comfortable with what it is doing. The script is commented to simplify this.**

This was mostly for fun and to help give others a tool to keep track of their tickets as they vote. Please learn what you can from it and modify it for your particular needs. Pull requests will be appreciated!

If you *really* appreciate this script, you can tip me DCR at DsfjHsSkgHCygnm5T68n1XNaCBXKD8D8DSZ, or you can enable OfficeSpaceMode in the script by setting `OfficeSpaceMode = 1`
This will send .001 DCR to my donation address each time the script finds tickets that have voted, which amounts to about 15 cents assuming DCR is worth $150. No pressure!

Have you seen my stapler?