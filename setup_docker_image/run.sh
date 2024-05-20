#!/bin/bash
#startup.sh file
/opt/kafka/bin/connect-distributed.sh /opt/kafka/config/sf-connect-distributed.properties &

# Sleep for 20 seconds
sleep 20

# Run the second command
curl -X POST -H "Content-Type: application/json" --data @config/SF_Connect.json http://localhost:8083/connectors