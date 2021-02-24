#!/bin/bash
echo "---Run Voted Ticket Notifier---"
echo "Press [CTRL+C] to stop.."
while :
do
  python3 VotedTicketNotifier.py
  # Run every 15 minutes
  sleep 900
done